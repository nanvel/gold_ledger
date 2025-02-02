from datetime import date, timedelta
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import PaymentStatus, PaymentType, ProductStatus
from app.db import PaymentTable, ProductTable, RetailerTable, SupplierTable


class Accounting:
    def __init__(self, session: Session):
        self._session = session

    def for_supplier(self, supplier_id: int, today: date):
        result = {}

        for payment_type in (PaymentType.CASH, PaymentType.RTGS, PaymentType.FINE):
            products = self._products_for_supplier(
                supplier_id=supplier_id,
                payment_type=payment_type,
            )

            for retailer_id, total in products:
                result[retailer_id] = result.get(retailer_id) or {}
                result[retailer_id][payment_type.slug] = {
                    "products": total,
                    "confirmed": 0,
                    "pending": 0,
                    "sum": 0,
                    "due_tomorrow_or_later": 0,
                    "due_today_or_later": 0,
                    "overdue": 0,
                    "due_today": 0,
                }

            payments_confirmed = self._payments_for_supplier(
                supplier_id=supplier_id,
                payment_type=payment_type,
                status=PaymentStatus.CONFIRMED,
            )
            for retailer_id, total in payments_confirmed:
                if retailer_id in result:
                    result[retailer_id][payment_type.slug]["confirmed"] = total
                else:
                    result[retailer_id] = {}
                    result[retailer_id][payment_type.slug] = {
                        "products": 0,
                        "confirmed": total,
                        "pending": 0,
                        "sum": 0,
                        "due_tomorrow_or_later": 0,
                        "due_today_or_later": 0,
                        "overdue": 0,
                        "due_today": 0,
                    }

            payments_pending = self._payments_for_supplier(
                supplier_id=supplier_id,
                payment_type=payment_type,
                status=PaymentStatus.PENDING,
            )
            for retailer_id, total in payments_pending:
                if retailer_id in result:
                    result[retailer_id][payment_type.slug]["pending"] = total
                else:
                    result[retailer_id] = {}
                    result[retailer_id][payment_type.slug] = {
                        "products": 0,
                        "confirmed": 0,
                        "pending": total,
                        "sum": 0,
                        "due_tomorrow_or_later": 0,
                        "due_today_or_later": 0,
                        "overdue": 0,
                        "due_today": 0,
                    }

            today_or_later = self._products_for_supplier(
                supplier_id=supplier_id,
                payment_type=payment_type,
                due_date=today - timedelta(days=1),
            )
            if today_or_later:
                tomorrow_or_later = self._products_for_supplier(
                    supplier_id=supplier_id,
                    payment_type=payment_type,
                    due_date=today + timedelta(days=1),
                )

                for retailer_id, total in tomorrow_or_later:
                    result[retailer_id][payment_type.slug][
                        "due_tomorrow_or_later"
                    ] = total
                for retailer_id, total in today_or_later:
                    result[retailer_id][payment_type.slug]["due_today_or_later"] = total

            for retailer_id, retailer in result.items():
                obj = retailer.get(payment_type.slug)
                if not obj:
                    continue
                obj["sum"] = obj["confirmed"] + obj["pending"] - obj["products"]
                if obj["sum"] < 0:
                    overdue_tomorrow = obj["sum"] + obj["due_tomorrow_or_later"]
                    if overdue_tomorrow < 0:
                        overdue_today = obj["sum"] + obj["due_today_or_later"]
                        if overdue_today < 0:
                            obj["overdue"] = -(max(overdue_today, obj["sum"]))

                        obj["due_today"] = min(
                            overdue_today - overdue_tomorrow,
                            -obj["sum"],
                        )

        if result:
            retailers = self._get_retailers(supplier_id=supplier_id)
            names = {retailer_id: name for retailer_id, name in retailers}
            for retailer_id, retailer in result.items():
                retailer["name"] = names.get(retailer_id)

        return result

    def for_retailer(self, retailer_id: int, today: date):
        result = {}

        for payment_type in (PaymentType.CASH, PaymentType.RTGS, PaymentType.FINE):
            products = self._products_for_retailer(
                retailer_id=retailer_id,
                payment_type=payment_type,
            )

            for supplier_id, total in products:
                result[supplier_id] = result.get(supplier_id) or {}
                result[supplier_id][payment_type.slug] = {
                    "products": total,
                    "confirmed": 0,
                    "pending": 0,
                    "sum": 0,
                    "due_tomorrow_or_later": 0,
                    "due_today_or_later": 0,
                    "overdue": 0,
                    "due_today": 0,
                }

            payments_confirmed = self._payments_for_retailer(
                retailer_id=retailer_id,
                payment_type=payment_type,
                status=PaymentStatus.CONFIRMED,
            )
            for supplier_id, total in payments_confirmed:
                if supplier_id in result:
                    result[supplier_id][payment_type.slug]["confirmed"] = total
                else:
                    result[supplier_id] = {}
                    result[supplier_id][payment_type.slug] = {
                        "products": 0,
                        "confirmed": total,
                        "pending": 0,
                        "sum": 0,
                        "due_tomorrow_or_later": 0,
                        "due_today_or_later": 0,
                        "overdue": 0,
                        "due_today": 0,
                    }

            payments_pending = self._payments_for_retailer(
                retailer_id=retailer_id,
                payment_type=payment_type,
                status=PaymentStatus.PENDING,
            )
            for supplier_id, total in payments_pending:
                if supplier_id in result:
                    result[supplier_id][payment_type.slug]["pending"] = total
                else:
                    result[supplier_id] = {}
                    result[supplier_id][payment_type.slug] = {
                        "products": 0,
                        "confirmed": 0,
                        "pending": total,
                        "sum": 0,
                        "due_tomorrow_or_later": 0,
                        "due_today_or_later": 0,
                        "overdue": 0,
                        "due_today": 0,
                    }

            today_or_later = self._products_for_retailer(
                retailer_id=retailer_id,
                payment_type=payment_type,
                due_date=today - timedelta(days=1),
            )
            if today_or_later:
                tomorrow_or_later = self._products_for_retailer(
                    retailer_id=retailer_id,
                    payment_type=payment_type,
                    due_date=today + timedelta(days=1),
                )

                for supplier_id, total in tomorrow_or_later:
                    result[supplier_id][payment_type.slug][
                        "due_tomorrow_or_later"
                    ] = total
                for supplier_id, total in today_or_later:
                    result[supplier_id][payment_type.slug]["due_today_or_later"] = total

            for supplier_id, supplier in result.items():
                obj = supplier.get(payment_type.slug)
                if not obj:
                    continue
                obj["sum"] = obj["confirmed"] + obj["pending"] - obj["products"]
                if obj["sum"] < 0:
                    overdue_tomorrow = obj["sum"] + obj["due_tomorrow_or_later"]
                    if overdue_tomorrow < 0:
                        overdue_today = obj["sum"] + obj["due_today_or_later"]
                        if overdue_today < 0:
                            obj["overdue"] = -(max(overdue_today, obj["sum"]))

                        obj["due_today"] = min(
                            overdue_today - overdue_tomorrow,
                            -obj["sum"],
                        )

        if result:
            retailers = self._get_suppliers(retailer_id=retailer_id)
            names = {supplier_id: name for supplier_id, name in retailers}
            for supplier_id, supplier in result.items():
                supplier["name"] = names.get(supplier_id)

        return result

    def _products_for_supplier(
        self,
        supplier_id: int,
        payment_type: PaymentType,
        due_date: Optional[date] = None,
    ):
        filters = [
            ProductTable.status == ProductStatus.CONFIRMED.value,
            ProductTable.payment_type == payment_type.value,
            ProductTable.supplier_id == supplier_id,
        ]
        if due_date:
            filters.append(ProductTable.payment_due_date > due_date)

        query = (
            self._session.query(
                ProductTable.retailer_id,
                (
                    func.sum(
                        ProductTable.payment_weight * ProductTable.quality / 100
                    ).label("total")
                    if payment_type == PaymentType.FINE
                    else func.sum(ProductTable.payment_amount).label("total")
                ),
            )
            .filter(*filters)
            .group_by(ProductTable.retailer_id)
        )

        return [(row.retailer_id, row.total) for row in query]

    def _products_for_retailer(
        self,
        retailer_id: int,
        payment_type: PaymentType,
        due_date: Optional[date] = None,
    ):
        filters = [
            ProductTable.status == ProductStatus.CONFIRMED.value,
            ProductTable.payment_type == payment_type.value,
            ProductTable.retailer_id == retailer_id,
        ]
        if due_date:
            filters.append(ProductTable.payment_due_date > due_date)

        query = (
            self._session.query(
                ProductTable.supplier_id,
                (
                    func.sum(
                        ProductTable.payment_weight * ProductTable.quality / 100
                    ).label("total")
                    if payment_type == PaymentType.FINE
                    else func.sum(ProductTable.payment_amount).label("total")
                ),
            )
            .filter(*filters)
            .group_by(ProductTable.supplier_id)
        )

        return [(row.supplier_id, row.total) for row in query]

    def _payments_for_supplier(
        self,
        supplier_id: int,
        payment_type: PaymentType,
        status: PaymentStatus = PaymentStatus.CONFIRMED,
    ):
        query = (
            self._session.query(
                PaymentTable.retailer_id,
                (
                    func.sum(PaymentTable.weight * PaymentTable.quality / 100).label(
                        "total"
                    )
                    if payment_type == PaymentType.FINE
                    else func.sum(PaymentTable.amount).label("total")
                ),
            )
            .filter(
                PaymentTable.status == status.value,
                PaymentTable.type == payment_type.value,
                PaymentTable.supplier_id == supplier_id,
            )
            .group_by(PaymentTable.retailer_id)
        )

        return [(row.retailer_id, row.total) for row in query]

    def _payments_for_retailer(
        self,
        retailer_id: int,
        payment_type: PaymentType,
        status: PaymentStatus = PaymentStatus.CONFIRMED,
    ):
        query = (
            self._session.query(
                PaymentTable.supplier_id,
                (
                    func.sum(PaymentTable.weight * PaymentTable.quality / 100).label(
                        "total"
                    )
                    if payment_type == PaymentType.FINE
                    else func.sum(PaymentTable.amount).label("total")
                ),
            )
            .filter(
                PaymentTable.status == status.value,
                PaymentTable.type == payment_type.value,
                PaymentTable.retailer_id == retailer_id,
            )
            .group_by(PaymentTable.supplier_id)
        )

        return [(row.supplier_id, row.total) for row in query]

    def _get_retailers(self, supplier_id):
        rows = (
            self._session.query(ProductTable.retailer_id, RetailerTable.name)
            .join(RetailerTable, RetailerTable.id == ProductTable.retailer_id)
            .filter(
                ProductTable.supplier_id == supplier_id,
                ProductTable.status == ProductStatus.CONFIRMED.value,
            )
            .distinct()
        )
        return [(row.retailer_id, row.name) for row in rows]

    def _get_suppliers(self, retailer_id):
        rows = (
            self._session.query(ProductTable.supplier_id, SupplierTable.name)
            .join(SupplierTable, SupplierTable.id == ProductTable.supplier_id)
            .filter(
                ProductTable.retailer_id == retailer_id,
                ProductTable.status == ProductStatus.CONFIRMED.value,
            )
            .distinct()
        )
        return [(row.supplier_id, row.name) for row in rows]
