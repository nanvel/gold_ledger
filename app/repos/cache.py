from sqlalchemy.orm import Session

from app.db import CacheTable
from app.models import Cache


class CacheRepo:
    def __init__(self, session: Session):
        self._session = session

    def create_or_update(self, cache: Cache):
        record = CacheTable(
            supplier_id=cache.supplier_id,
            retailer_id=cache.retailer_id,
            cash_products=cache.cash_products,
            cash_payments=cache.cash_payments,
            cash_due_date=cache.cash_due_date,
            cash_to_pay=cache.cash_to_pay,
            rtgs_products=cache.rtgs_products,
            rtgs_payments=cache.rtgs_payments,
            rtgs_due_date=cache.rtgs_due_date,
            rtgs_to_pay=cache.rtgs_to_pay,
            fine_products=cache.fine_products,
            fine_payments=cache.fine_payments,
            fine_due_date=cache.fine_due_date,
            fine_to_pay=cache.fine_to_pay,
        )

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return record.id
