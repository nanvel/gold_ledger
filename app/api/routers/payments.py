from dataclasses import replace
from datetime import date
from decimal import Decimal
from typing import Optional, Tuple

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.container import Container
from app.models import Activity, ActivityType, PaymentType, User
from app.repos.payments import PaymentDetailsItem, PaymentSearchItem
from app.repos.uow import UnitOfWork
from app.use_cases.add_payment import AddPayment
from .auth import get_active_user

router = APIRouter()


class PaymentForm(BaseModel):
    type: PaymentType
    date: date
    weight: Optional[Decimal] = Field(None, gt=0)
    quality: Optional[Decimal] = Field(None, gt=0, le=100)
    amount: Optional[Decimal] = Field(None, gt=0)
    supplier_id: int


class PaymentResponse(BaseModel):
    success: bool


@router.post("/payments", status_code=201)
@inject
def add_payment(
    item: PaymentForm,
    user: User = Depends(get_active_user),
    use_case: AddPayment = Depends(Provide[Container.add_payment]),
) -> PaymentResponse:
    if not user.is_retailer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user is not a retailer.",
        )

    if item.type == PaymentType.CASH:
        if item.weight is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "type": "weight_required",
                        "loc": ["body", "weight"],
                        "msg": "Weight is required for fine payment.",
                    }
                ],
            )

        if item.quality is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "type": "quality_required",
                        "loc": ["body", "quality"],
                        "msg": "Quality is required for fine payment.",
                    }
                ],
            )
    else:
        if item.amount is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "type": "amount_required",
                        "loc": ["body", "amount"],
                        "msg": "Amount is required for cash payment.",
                    }
                ],
            )

    use_case(
        supplier_id=item.supplier_id,
        retailer_id=user.retailer_id,
        creator_id=user.id,
        type_=item.type,
        date_=item.date,
        weight=item.weight,
        quality=item.quality,
        amount=item.amount,
    )

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


@router.get("/payments/{payment_id}")
@inject
def get_payment(
    payment_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> PaymentDetailsItem:
    with uow:
        payment_details = uow.payments.details(payment_id)

        if not payment_details or (
            payment_details.supplier.id != user.supplier_id
            and payment_details.retailer.id != user.retailer_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The payment was not found",
            )

        return payment_details


class UpdateResponse(BaseModel):
    success: bool


@router.post("/payments/{payment_id}/confirm")
@inject
def confirm_payment(
    payment_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    activity_message_factory=Depends(Provide[Container.activity_message_factory]),
) -> UpdateResponse:
    with uow:
        payment = uow.payments.by_id(payment_id)

        if not payment or payment.supplier_id != user.supplier_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The payment was not found",
            )

        payment = payment.confirm(user)
        uow.payments.update(payment)

        activity = Activity(
            id=0,
            type=ActivityType.PAYMENT_CONFIRMED,
            user_id=user.id,
            supplier_id=payment.supplier_id,
            retailer_id=payment.retailer_id,
            product_id=None,
            payment_id=payment.id,
            message="",
        )
        activity = replace(
            activity,
            message=activity_message_factory.from_activity(activity, uow),
        )
        uow.activities.create(activity)

    return UpdateResponse(success=True)


@router.post("/payments/{payment_id}/reject")
@inject
def reject_payment(
    payment_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    activity_message_factory=Depends(Provide[Container.activity_message_factory]),
) -> UpdateResponse:
    with uow:
        payment = uow.payments.by_id(payment_id)

        if not payment or payment.supplier_id != user.supplier_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The payment was not found",
            )

        payment = payment.reject(user)
        uow.payments.update(payment)

        activity = Activity(
            id=0,
            type=ActivityType.PAYMENT_REJECTED,
            user_id=user.id,
            supplier_id=payment.supplier_id,
            retailer_id=payment.retailer_id,
            product_id=None,
            payment_id=payment.id,
            message="",
        )
        activity = replace(
            activity,
            message=activity_message_factory.from_activity(activity, uow),
        )
        uow.activities.create(activity)

    return UpdateResponse(success=True)


@router.post("/payments/{payment_id}/cancel")
@inject
def cancel_payment(
    payment_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    activity_message_factory=Depends(Provide[Container.activity_message_factory]),
) -> UpdateResponse:
    with uow:
        payment = uow.payments.by_id(payment_id)

        if not payment or payment.retailer_id != user.retailer_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The payment was not found",
            )

        payment = payment.cancel(user)
        uow.payments.update(payment)

        activity = Activity(
            id=0,
            type=ActivityType.PAYMENT_CANCELLED,
            user_id=user.id,
            supplier_id=payment.supplier_id,
            retailer_id=payment.retailer_id,
            product_id=None,
            payment_id=payment.id,
            message="",
        )
        activity = replace(
            activity,
            message=activity_message_factory.from_activity(activity, uow),
        )
        uow.activities.create(activity)

    return UpdateResponse(success=True)
