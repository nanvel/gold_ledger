from sqlalchemy.orm import Session

from app.db import CacheTable, PaymentTable, ProductTable
from app.models import PaymentStatus, ProductStatus, Cache


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
        record.cash_due_date = cache.cash_due_date
        record.cash_to_pay = cache.cash_to_pay
        record.rtgs_products = cache.rtgs_products
        record.rtgs_payments = cache.rtgs_payments
        record.rtgs_due_date = cache.rtgs_due_date
        record.rtgs_to_pay = cache.rtgs_to_pay
        record.fine_products = cache.fine_products
        record.fine_payments = cache.fine_payments
        record.fine_due_date = cache.fine_due_date
        record.fine_to_pay = cache.fine_to_pay

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
