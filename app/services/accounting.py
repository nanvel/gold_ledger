from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal
from typing import Dict, List, Optional

from sqlalchemy import text

from app.models import PaymentStatus, PaymentType, ProductStatus


@dataclass(frozen=True)
class AccountingState:
    payment_type: PaymentType
    payments: Decimal
    products: Decimal
    due_date: Optional[date]
    amount: Optional[Decimal]


class AccountingService:
    def __init__(self, db):
        self._db = db

    def compute(self, supplier_id: int, retailer_id: int) -> List[AccountingState]:
        payment = self._payments(supplier_id=supplier_id, retailer_id=retailer_id)
        res = []
        for payment_type in PaymentType:
            products = self._products(
                supplier_id=supplier_id,
                retailer_id=retailer_id,
                payment_type=payment_type,
            )
            state = AccountingState(
                payment_type=payment_type,
                payments=payment[payment_type.value],
                products=sum(i for _, i in products) if products else Decimal(0),
                due_date=None,
                amount=None,
            )

            s = Decimal(0)
            p = payment[payment_type.value]
            for due_date, total_amount in products:
                if s + total_amount > p:
                    state = replace(
                        state, due_date=due_date, amount=s + total_amount - p
                    )
                    break
                s += total_amount

            res.append(state)

        return res

    def _payments(self, supplier_id: int, retailer_id: int) -> Dict[int, Decimal]:
        rows = self._db.execute(
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

        for payment_type in PaymentType:
            if payment_type not in res:
                res[int(payment_type)] = Decimal(0)

        return res

    def _products(
        self, supplier_id: int, retailer_id: int, payment_type: PaymentType
    ) -> Dict[date, Decimal]:
        rows = self._db.execute(
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
