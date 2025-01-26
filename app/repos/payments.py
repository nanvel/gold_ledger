from sqlalchemy.orm import Session

from app.db import PaymentTable
from app.models import Payment


class PaymentsRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, payment: Payment) -> int:
        record = PaymentTable(
            date=payment.date,
            type=payment.type.value,
            weight=payment.weight,
            quality=payment.quality,
            rate_per_gram=payment.rate_per_gram,
            total_amount=payment.total_amount,
            supplier_id=payment.supplier_id,
            retailer_id=payment.retailer_id,
            creator_id=payment.creator_id,
        )

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return record.id
