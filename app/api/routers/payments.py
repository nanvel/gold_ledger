from datetime import date
from decimal import Decimal
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator

from app.container import Container
from app.models import PaymentType, Payment, User
from app.repos.uow import UnitOfFork
from .auth import get_active_user

router = APIRouter()


class PaymentForm(BaseModel):
    type: PaymentType
    date: date
    weight: Optional[Decimal] = Field(None, gt=0)
    quality: Optional[Decimal] = Field(None, ge=0, le=100)
    rate_per_gram: Optional[Decimal] = Field(None, gt=0)
    total_amount: Decimal = Field(..., gt=0)
    supplier_id: int


class PaymentResponse(BaseModel):
    success: bool


@router.post("/payments", status_code=201)
@inject
def create_payment(
    item: PaymentForm,
    user: User = Depends(get_active_user),
    uow: UnitOfFork = Depends(Provide[Container.uow]),
) -> PaymentResponse:
    if not user.is_retailer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user is not a retailer.",
        )

    with uow:
        supplier = uow.suppliers.by_id(item.supplier_id)

        if supplier is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The supplier store was not found.",
            )

        payment = Payment(
            id=0,
            type=item.type,
            date=item.date,
            weight=item.weight,
            quality=item.quality,
            rate_per_gram=item.rate_per_gram,
            total_amount=item.total_amount,
            retailer_id=user.retailer_id,
            supplier_id=supplier.id,
            creator_id=user.id,
        )
        uow.payments.create(payment)

    return PaymentResponse(success=True)
