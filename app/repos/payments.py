from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db import PaymentTable
from app.models import (
    Payment,
    PaymentOrderBy,
    PaymentStatus,
    PaymentType,
    Timestamp,
)


@dataclass(frozen=True)
class PaymentSearchItem:
    id: int
    type: str
    date: str
    weight: Optional[Decimal]
    quality: Optional[Decimal]
    amount: Optional[Decimal]
    created_at: int
    confirmed_by: Optional[int]
    rejected_by: Optional[int]
    cancelled_by: Optional[int]
    status: str


@dataclass(frozen=True)
class PaymentDetailsItem:
    id: int
    type: str
    date: str
    weight: Optional[Decimal]
    quality: Optional[Decimal]
    amount: Optional[Decimal]
    supplier_id: int
    retailer_id: int
    creator_id: int
    confirmed_by: Optional[int]
    rejected_by: Optional[int]
    cancelled_by: Optional[int]
    created_at: int
    status: str


@dataclass(frozen=True)
class PaymentsStats:
    total_paid: Decimal
    total_pending: Decimal
    number_paid: int
    number_pending: int


class PaymentsRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, payment: Payment) -> int:
        record = PaymentTable(
            date=payment.date,
            type=payment.type.value,
            weight=payment.weight,
            quality=payment.quality,
            amount=payment.amount,
            supplier_id=payment.supplier_id,
            retailer_id=payment.retailer_id,
            creator_id=payment.creator_id,
            status=payment.status.value,
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
            record.cancelled_by = payment.cancelled_by
            record.status = payment.status.value

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
                amount=record.amount,
                supplier_id=record.supplier_id,
                retailer_id=record.retailer_id,
                creator_id=record.creator_id,
                confirmed_by=record.confirmed_by,
                rejected_by=record.rejected_by,
                cancelled_by=record.cancelled_by,
            )

    def details(self, payment_id: int) -> Optional[PaymentDetailsItem]:
        record = self._session.query(PaymentTable).filter_by(id=payment_id).first()

        if record:
            return PaymentDetailsItem(
                id=record.id,
                type=PaymentType(record.type).label,
                date=record.date.isoformat(),
                weight=record.weight,
                quality=record.quality,
                amount=record.amount,
                supplier_id=record.supplier_id,
                retailer_id=record.retailer_id,
                creator_id=record.creator_id,
                confirmed_by=record.confirmed_by,
                rejected_by=record.rejected_by,
                cancelled_by=record.cancelled_by,
                created_at=int(Timestamp.from_datetime(record.created_at)),
                status=PaymentStatus(record.status).label,
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

        return (
            total,
            tuple(
                PaymentSearchItem(
                    id=record.id,
                    type=PaymentType(record.type).slug,
                    date=record.date.isoformat(),
                    weight=record.weight,
                    quality=record.quality,
                    amount=record.amount,
                    created_at=int(Timestamp.from_datetime(record.created_at)),
                    confirmed_by=record.confirmed_by,
                    rejected_by=record.rejected_by,
                    cancelled_by=record.cancelled_by,
                    status=PaymentStatus(record.status).slug,
                )
                for record in records
            ),
        )

    def stats(
        self,
        supplier_id: Optional[int],
        retailer_id: Optional[int],
    ) -> PaymentsStats:
        # TODO: rewrite, user cancelled as well
        query = self._session.query(
            func.sum(PaymentTable.amount).label("total"),
            func.count(PaymentTable.id).label("count"),
        )

        if supplier_id:
            query = query.filter(PaymentTable.supplier_id == supplier_id)
        if retailer_id:
            query = query.filter(PaymentTable.retailer_id == retailer_id)

        total_paid, number_paid = query.filter(
            PaymentTable.confirmed_by.isnot(None)
        ).first() or (Decimal(0), 0)

        total_pending, number_pending = query.filter(
            PaymentTable.confirmed_by.is_(None),
            PaymentTable.rejected_by.is_(None),
        ).first() or (Decimal(0), 0)

        return PaymentsStats(
            total_paid=total_paid or Decimal(0),
            total_pending=total_pending or Decimal(0),
            number_paid=number_paid or 0,
            number_pending=number_pending or 0,
        )
