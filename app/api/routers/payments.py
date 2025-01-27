from dataclasses import replace
from datetime import date
from decimal import Decimal
from typing import Optional, Tuple

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.container import Container
from app.models import PaymentType, Payment, User
from app.repos.payments import PaymentSearchItem
from app.repos.uow import UnitOfWork
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
    uow: UnitOfWork = Depends(Provide[Container.uow]),
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
            confirmed_by=None,
            rejected_by=None,
        )
        payment.validate()
        uow.payments.create(payment)

    return PaymentResponse(success=True)


class PaymentsResponse(BaseModel):
    total: int
    items: Tuple[PaymentSearchItem, ...]


@router.get("/payments")
@inject
def get_payments(
    retailer_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    limit: int = 20,
    offset: int = 0,
) -> PaymentsResponse:
    if user.is_supplier:
        supplier_id = user.supplier_id
    else:
        retailer_id = user.retailer_id

    with uow:
        total, items = uow.payments.filter(
            supplier_id=supplier_id,
            retailer_id=retailer_id,
            limit=limit,
            offset=offset,
        )

    return PaymentsResponse(total=total, items=items)


class UpdateResponse(BaseModel):
    success: bool


@router.post("/payments/{payment_id}/confirm")
@inject
def confirm_payment(
    payment_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> UpdateResponse:
    with uow:
        payment = uow.payments.by_id(payment_id)

        if not payment or payment.supplier_id != user.supplier_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The payment was not found.",
            )

        assert payment.rejected_by is None
        assert payment.confirmed_by is None

        payment = replace(payment, confirmed_by=user.id)

        uow.payments.update(payment)

    return UpdateResponse(success=True)


@router.post("/payments/{payment_id}/reject")
@inject
def reject_payment(
    payment_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> UpdateResponse:
    with uow:
        payment = uow.payments.by_id(payment_id)

        if not payment or payment.supplier_id != user.supplier_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The payment was not found.",
            )

        assert payment.rejected_by is None
        assert payment.confirmed_by is None

        payment = replace(payment, rejected_by=user.id)

        uow.payments.update(payment)

    return UpdateResponse(success=True)
