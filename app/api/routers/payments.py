from dataclasses import replace
from datetime import date
from decimal import Decimal
from typing import Optional, Tuple

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.container import Container
from app.models import Activity, ActivityType, PaymentType, Payment, User
from app.repos.payments import PaymentDetailsItem, PaymentSearchItem
from app.repos.uow import UnitOfWork
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
def create_payment(
    item: PaymentForm,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    activity_message_factory=Depends(Provide[Container.activity_message_factory]),
) -> PaymentResponse:
    if not user.is_retailer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user is not a retailer.",
        )

    if item.type == PaymentType.CASH:
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
    else:
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
            amount=item.amount,
            retailer_id=user.retailer_id,
            supplier_id=supplier.id,
            creator_id=user.id,
            confirmed_by=None,
            rejected_by=None,
        )
        payment.validate()
        payment_id = uow.payments.create(payment)

        activity = Activity(
            id=0,
            type=ActivityType.PAYMENT_ADDED,
            user_id=user.id,
            supplier_id=supplier.id,
            retailer_id=user.retailer_id,
            product_id=None,
            payment_id=payment_id,
            message="",
        )
        activity = replace(
            activity,
            message=activity_message_factory.from_activity(activity, uow),
        )
        uow.activities.create(activity)

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
            payment_details.supplier_id != user.supplier_id
            and payment_details.retailer_id != user.retailer_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The payment was not found.",
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
                detail="The payment was not found.",
            )

        assert payment.rejected_by is None
        assert payment.confirmed_by is None

        payment = replace(payment, confirmed_by=user.id)

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
                detail="The payment was not found.",
            )

        assert payment.rejected_by is None
        assert payment.confirmed_by is None

        payment = replace(payment, rejected_by=user.id)

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


class SummaryResponse(BaseModel):
    total_payments: Decimal
    total_products: Decimal
    total_pending: Decimal
    total_overdue: Decimal


@router.get("/payments-summary")
@inject
def payments_summary(
    supplier_id: Optional[int] = None,
    retailer_id: Optional[int] = None,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> SummaryResponse:
    if user.supplier_id:
        supplier_id = user.supplier_id
    elif user.retailer_id:
        retailer_id = user.retailer_id

    with uow:
        product_stats = uow.products.stats(
            supplier_id=supplier_id, retailer_id=retailer_id
        )
        payment_stats = uow.payments.stats(
            supplier_id=supplier_id, retailer_id=retailer_id
        )

        total_pending = product_stats.total_received - payment_stats.total_paid
        overdue = Decimal(0)
        if total_pending > 0 and total_pending > product_stats.total_ontime:
            if total_pending > product_stats.total_ontime:
                overdue = total_pending - product_stats.total_ontime

        return SummaryResponse(
            total_payments=payment_stats.total_paid,
            total_products=product_stats.total_received,
            total_pending=total_pending,
            total_overdue=overdue,
        )
