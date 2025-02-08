from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import PaymentTable
from app.models import (
    DisplayPayment,
    DisplayRetailer,
    DisplaySupplier,
    DisplayUser,
    Payment,
    PaymentOrderBy,
    PaymentStatus,
    PaymentType,
    Timestamp,
)


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
            note=payment.note,
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
                note=record.note,
                supplier_id=record.supplier_id,
                retailer_id=record.retailer_id,
                creator_id=record.creator_id,
                confirmed_by=record.confirmed_by,
                rejected_by=record.rejected_by,
                cancelled_by=record.cancelled_by,
            )

    def display(self, payment_id: int) -> Optional[DisplayPayment]:
        record = self._session.query(PaymentTable).filter_by(id=payment_id).first()

        if record:
            return DisplayPayment(
                id=record.id,
                type=PaymentType(record.type).slug,
                date=record.date.isoformat(),
                weight=record.weight,
                quality=record.quality,
                amount=record.amount,
                note=record.note,
                supplier=DisplaySupplier(
                    id=record.supplier.id, name=record.supplier.name
                ),
                retailer=DisplayRetailer(
                    id=record.retailer.id, name=record.retailer.name
                ),
                creator=DisplayUser(
                    id=record.creator.id,
                    name=record.creator.name,
                    email=record.creator.username,
                ),
                confirmed_by=(
                    DisplayUser(
                        id=record.confirmed_by_user.id,
                        name=record.confirmed_by_user.name,
                        email=record.confirmed_by_user.username,
                    )
                    if record.confirmed_by
                    else None
                ),
                rejected_by=(
                    DisplayUser(
                        id=record.rejected_by_user.id,
                        name=record.rejected_by_user.name,
                        email=record.rejected_by_user.username,
                    )
                    if record.rejected_by
                    else None
                ),
                cancelled_by=(
                    DisplayUser(
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
        status: Optional[PaymentStatus],
        limit: int,
        offset: int,
        order_by: PaymentOrderBy = PaymentOrderBy.CREATED,
        reverse: bool = True,
    ) -> Tuple[int, Tuple[DisplayPayment, ...]]:
        query = self._session.query(PaymentTable)

        if supplier_id:
            query = query.filter(PaymentTable.supplier_id == supplier_id)
        if retailer_id:
            query = query.filter(PaymentTable.retailer_id == retailer_id)
        if status:
            query = query.filter(PaymentTable.status == status.value)

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
                DisplayPayment(
                    id=record.id,
                    type=PaymentType(record.type).slug,
                    date=record.date.isoformat(),
                    weight=record.weight,
                    quality=record.quality,
                    amount=record.amount,
                    note=record.note,
                    created_at=int(Timestamp.from_datetime(record.created_at)),
                    status=PaymentStatus(record.status).slug,
                    retailer=DisplayRetailer(
                        id=record.retailer.id, name=record.retailer.name
                    ),
                    supplier=DisplaySupplier(
                        id=record.supplier.id, name=record.supplier.name
                    ),
                    creator=DisplayUser(
                        id=record.creator.id,
                        name=record.creator.name,
                        email=record.creator.username,
                    ),
                    confirmed_by=(
                        DisplayUser(
                            id=record.confirmed_by_user.id,
                            name=record.confirmed_by_user.name,
                            email=record.confirmed_by_user.username,
                        )
                        if record.confirmed_by
                        else None
                    ),
                    rejected_by=(
                        DisplayUser(
                            id=record.rejected_by_user.id,
                            name=record.rejected_by_user.name,
                            email=record.rejected_by_user.username,
                        )
                        if record.rejected_by
                        else None
                    ),
                    cancelled_by=(
                        DisplayUser(
                            id=record.cancelled_by_user.id,
                            name=record.cancelled_by_user.name,
                            email=record.cancelled_by_user.username,
                        )
                        if record.cancelled_by
                        else None
                    ),
                )
                for record in records
            ),
        )
