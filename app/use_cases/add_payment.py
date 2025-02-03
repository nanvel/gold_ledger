from datetime import date
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status

from app.models import Payment, PaymentType
from app.repos.uow import UnitOfWork


class AddPayment:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(
        self,
        supplier_id: int,
        retailer_id: int,
        creator_id: int,
        type_: PaymentType,
        date_: date,
        weight: Optional[Decimal],
        quality: Optional[Decimal],
        amount: Optional[Decimal],
    ):
        with self._uow:
            supplier = self._uow.suppliers.by_id(supplier_id)

            if supplier is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The supplier store was not found.",
                )

            payment = Payment(
                id=0,
                type=type_,
                date=date_,
                weight=weight,
                quality=quality,
                amount=amount,
                retailer_id=retailer_id,
                supplier_id=supplier.id,
                creator_id=creator_id,
                confirmed_by=None,
                rejected_by=None,
                cancelled_by=None,
            )
            payment.validate()
            self._uow.payments.create(payment)
