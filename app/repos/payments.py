from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import PaymentTable
from app.models import (
    Payment,
    PaymentOrderBy,
    PaymentType,
    Timestamp,
)


@dataclass(frozen=True)
class PaymentSearchItem:
    id: int
    type: str
    date: str
    weight: Decimal
    quality: Decimal
    rate_per_gram: Decimal
    total_amount: Decimal
    created_at: int


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

    def update(self, payment: Payment) -> None:
        record = self._session.query(PaymentTable).filter_by(id=payment.id).first()

        if record:
            record.confirmed_by = payment.confirmed_by
            record.rejected_by = payment.rejected_by

            self._session.commit()

    def by_id(self, payment_id: int) -> Optional[Payment]:
        record = self._session.query(PaymentTable).filter_by(id=payment_id).first()

        if record:
            return Payment(
                id=record.id,
                type=PaymentType(record.type),
                date=record.date,
                weight=record.weight,
                quality=record.quality,
                rate_per_gram=record.rate_per_gram,
                total_amount=record.total_amount,
                supplier_id=record.supplier_id,
                retailer_id=record.retailer_id,
                creator_id=record.creator_id,
                confirmed_by=record.confirmed_by,
                rejected_by=record.rejected_by,
            )

    def filter(
        self,
        supplier_id: Optional[int],
        retailer_id: Optional[int],
        limit: int,
        offset: int,
        order_by: PaymentOrderBy = PaymentOrderBy.CREATED,
        reverse: bool = True,
    ) -> Tuple[int, Tuple[PaymentSearchItem, ...]]:
        query = self._session.query(PaymentTable)

        if supplier_id:
            query = query.filter(PaymentTable.supplier_id == supplier_id)
        if retailer_id:
            query = query.filter(PaymentTable.retailer_id == retailer_id)

        total = query.count()

        order_by_field = (
            PaymentTable.created_at
            if order_by == PaymentOrderBy.CREATED
            else PaymentTable.id
        )

        if reverse:
            order_by_field = order_by_field.desc()

        records = query.order_by(order_by_field).offset(offset).limit(limit)

        return total, tuple(
            PaymentSearchItem(
                id=record.id,
                type=PaymentType(record.type).slug,
                date=record.date.isoformat(),
                weight=record.weight,
                quality=record.quality,
                rate_per_gram=record.rate_per_gram,
                total_amount=record.total_amount,
                created_at=int(Timestamp.from_datetime(record.created_at)),
            )
            for record in records
        )
