from decimal import Decimal

from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import CacheTable, PaymentTable, ProductTable
from app.models import (
    Cache,
    DisplayCache,
    DisplayDuePayment,
    DisplayRetailer,
    DisplaySupplier,
    PaymentStatus,
    PaymentType,
    ProductStatus,
)


class CacheRepo:
    def __init__(self, session: Session):
        self._session = session

    def create_or_update(self, cache: Cache):
        record = (
            self._session.query(CacheTable)
            .filter(
                CacheTable.supplier_id == cache.supplier_id,
                CacheTable.retailer_id == cache.retailer_id,
            )
            .first()
        )

        if not record:
            record = CacheTable(
                supplier_id=cache.supplier_id,
                retailer_id=cache.retailer_id,
            )

        record.cash_products = cache.cash_products
        record.cash_payments = cache.cash_payments
        record.rtgs_products = cache.rtgs_products
        record.rtgs_payments = cache.rtgs_payments
        record.fine_products = cache.fine_products
        record.fine_payments = cache.fine_payments
        record.due_payments = [
            {
                "type": payment.type.value,
                "date": payment.date.isoformat(),
                "amount": str(payment.amount),
            }
            for payment in cache.due_payments
        ]

        self._session.add(record)
        self._session.commit()

    def all_keys(self):
        res = set()

        rows = (
            self._session.query(ProductTable.supplier_id, ProductTable.retailer_id)
            .where(ProductTable.status == ProductStatus.CONFIRMED.value)
            .distinct()
        )

        for row in rows:
            res.add((row.supplier_id, row.retailer_id))

        rows = (
            self._session.query(PaymentTable.supplier_id, PaymentTable.retailer_id)
            .where(PaymentTable.status == PaymentStatus.CONFIRMED.value)
            .distinct()
        )

        for row in rows:
            res.add((row.supplier_id, row.retailer_id))

        return res

    def filter(
        self, supplier_id: Optional[int], retailer_id: Optional[int]
    ) -> List[DisplayCache]:
        assert supplier_id or retailer_id
        filters = []
        if supplier_id:
            filters.append(CacheTable.supplier_id == supplier_id)
        if retailer_id:
            filters.append(CacheTable.retailer_id == retailer_id)
        rows = self._session.query(CacheTable).filter(*filters)

        return [
            DisplayCache(
                supplier=DisplaySupplier(id=row.supplier.id, name=row.supplier.name),
                retailer=DisplayRetailer(id=row.retailer.id, name=row.retailer.name),
                cash_products=row.cash_products,
                cash_payments=row.cash_payments,
                rtgs_products=row.rtgs_products,
                rtgs_payments=row.rtgs_payments,
                fine_products=row.fine_products,
                fine_payments=row.fine_payments,
                due_payments=[
                    DisplayDuePayment(
                        type=PaymentType(payment["type"]).slug,
                        date=payment["date"],
                        amount=Decimal(payment["amount"]),
                    )
                    for payment in row.due_payments
                ],
            )
            for row in rows
        ]
