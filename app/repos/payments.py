from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import PaymentTable
from app.models import (
    Payment,
    PaymentOrderBy,
    PaymentStatus,
    PaymentType,
    Timestamp,
)


@dataclass(frozen=True)
class PaymentStore:
    id: int
    name: str


@dataclass(frozen=True)
class PaymentUser:
    id: int
    name: str
    email: str


@dataclass(frozen=True)
class PaymentSearchItem:
    id: int
    type: str
    date: str
    weight: Optional[Decimal]
    quality: Optional[Decimal]
    amount: Optional[Decimal]
    created_at: int
    status: str
    retailer: PaymentStore
    supplier: PaymentStore


@dataclass(frozen=True)
class PaymentDetailsItem:
    id: int
    type: str
    date: str
    weight: Optional[Decimal]
    quality: Optional[Decimal]
    amount: Optional[Decimal]
    supplier: PaymentStore
    retailer: PaymentStore
    creator: PaymentUser
    confirmed_by: Optional[PaymentUser]
    rejected_by: Optional[PaymentUser]
    cancelled_by: Optional[PaymentUser]
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
                supplier=PaymentStore(id=record.supplier.id, name=record.supplier.name),
                retailer=PaymentStore(id=record.retailer.id, name=record.retailer.name),
                creator=PaymentUser(
                    id=record.creator.id,
                    name=record.creator.name,
                    email=record.creator.username,
                ),
                confirmed_by=(
                    PaymentUser(
                        id=record.confirmed_by_user.id,
                        name=record.confirmed_by_user.name,
                        email=record.confirmed_by_user.username,
                    )
                    if record.confirmed_by
                    else None
                ),
                rejected_by=(
                    PaymentUser(
                        id=record.rejected_by_user.id,
                        name=record.rejected_by_user.name,
                        email=record.rejected_by_user.username,
                    )
                    if record.rejected_by
                    else None
                ),
                cancelled_by=(
                    PaymentUser(
                        id=record.cancelled_by_user.id,
                        name=record.cancelled_by_user.name,
                        email=record.cancelled_by_user.username,
                    )
                    if record.cancelled_by
                    else None
                ),
                created_at=int(Timestamp.from_datetime(record.created_at)),
                status=PaymentStatus(record.status).slug,
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
                    status=PaymentStatus(record.status).slug,
                    retailer=PaymentStore(
                        id=record.retailer.id, name=record.retailer.name
                    ),
                    supplier=PaymentStore(
                        id=record.supplier.id, name=record.supplier.name
                    ),
                )
                for record in records
            ),
        )
