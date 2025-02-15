from dataclasses import replace
from datetime import date
from decimal import Decimal
from typing import Dict

from sqlalchemy import text

from app.models import Cache, DuePayment, PaymentStatus, PaymentType, ProductStatus


class AccountingService:
    def __init__(self, db):
        self._db = db

    def compute(self, supplier_id: int, retailer_id: int) -> Cache:
        with self._db.session() as session:
            payments = self._payments(
                session, supplier_id=supplier_id, retailer_id=retailer_id
            )
            cache = Cache(
                supplier_id=supplier_id,
                retailer_id=retailer_id,
                cash_products=Decimal(0),
                cash_payments=payments.get(PaymentType.CASH.value, Decimal(0)),
                rtgs_products=Decimal(0),
                rtgs_payments=payments.get(PaymentType.RTGS.value, Decimal(0)),
                fine_products=Decimal(0),
                fine_payments=payments.get(PaymentType.FINE.value, Decimal(0)),
                due_payments=[],
            )

            due_payments = []

            for payment_type in PaymentType:
                products = self._products(
                    session,
                    supplier_id=supplier_id,
                    retailer_id=retailer_id,
                    payment_type=payment_type,
                )
                products_total = sum(i for _, i in products) if products else Decimal(0)

                s = Decimal(0)
                p = payments.get(payment_type.value, Decimal(0))
                for dd, total_amount in products:
                    if s + total_amount > p:
                        to_pay = s + total_amount - p
                        due_payments.append(
                            DuePayment(
                                type=payment_type,
                                date=dd,
                                amount=s + total_amount - p,
                            )
                        )
                        s -= to_pay
                    s += total_amount

                cache = replace(
                    cache,
                    **{
                        f"{payment_type.slug}_products": products_total,
                    },
                )

        return replace(cache, due_payments=due_payments)

    def _payments(
        self, session, supplier_id: int, retailer_id: int
    ) -> Dict[int, Decimal]:
        rows = session.execute(
            text(
                """SELECT type,
                          sum(coalesce(amount, 0)) AS total_amount,
                          sum(coalesce(weight, 0) * coalesce(quality, 0) / 100) AS total_fine
                    FROM payments
                    WHERE status = :status
                      AND supplier_id = :supplier_id
                      AND retailer_id = :retailer_id
                    GROUP BY type;"""
            ),
            {
                "supplier_id": supplier_id,
                "retailer_id": retailer_id,
                "status": PaymentStatus.CONFIRMED.value,
            },
        )
        res = {}
        for payment_type, total_amount, total_fine in rows:
            res[payment_type] = total_amount or total_fine

        return res

    def _products(
        self, session, supplier_id: int, retailer_id: int, payment_type: PaymentType
    ) -> Dict[date, Decimal]:
        rows = session.execute(
            text(
                """SELECT payment_due_date, sum({}) AS total_amount
                    FROM products
                    WHERE supplier_id = :supplier_id
                      AND retailer_id = :retailer_id
                      AND status = :status
                      AND payment_type = :payment_type
                    GROUP BY payment_due_date
                    ORDER BY payment_due_date;""".format(
                    "payment_weight * payment_quality / 100"
                    if payment_type == PaymentType.FINE
                    else "payment_amount"
                )
            ),
            {
                "supplier_id": supplier_id,
                "retailer_id": retailer_id,
                "status": ProductStatus.CONFIRMED.value,
                "payment_type": payment_type.value,
            },
        )

        return [(due_date, total_amount) for due_date, total_amount in rows]
