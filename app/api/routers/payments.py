from datetime import date
from decimal import Decimal
from typing import Optional, Tuple

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status as status_codes
from pydantic import BaseModel, Field

from app.container import Container
from app.models import PaymentStatus, PaymentType, DisplayPayment, User
from app.repos.uow import UnitOfWork
from app.use_cases.add_payment import AddPayment
from app.use_cases.cancel_payment import CancelPayment
from app.use_cases.confirm_payment import ConfirmPayment
from app.use_cases.reject_payment import RejectPayment
from .auth import get_active_user

router = APIRouter()


class PaymentForm(BaseModel):
    type: PaymentType
    date: date
    weight: Optional[Decimal] = Field(None, gt=0)
    quality: Optional[Decimal] = Field(None, gt=0, le=100)
    amount: Optional[Decimal] = Field(None, gt=0)
    note: Optional[str] = Field(None, max_length=120)
    supplier_id: int


class EmptyResponse(BaseModel):
    success: bool


@router.post("/payments", status_code=201)
@inject
def add_payment(
    item: PaymentForm,
    user: User = Depends(get_active_user),
    use_case: AddPayment = Depends(Provide[Container.add_payment]),
) -> EmptyResponse:
    if not user.is_retailer:
        raise HTTPException(
            status_code=status_codes.HTTP_403_FORBIDDEN,
            detail="The user is not a retailer.",
        )

    if item.type == PaymentType.FINE:
        if item.weight is None:
            raise HTTPException(
                status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY,
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
                status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY,
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
                status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY,
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
        note=item.note,
    )

    return EmptyResponse(success=True)


class PaymentsResponse(BaseModel):
    total: int
    items: Tuple[DisplayPayment, ...]


@router.get("/payments")
@inject
def get_payments(
    retailer_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    status: Optional[PaymentStatus] = None,
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
            status=status,
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
) -> DisplayPayment:
    with uow:
        payment_details = uow.payments.display(payment_id)

        if not payment_details or (
            payment_details.supplier.id != user.supplier_id
            and payment_details.retailer.id != user.retailer_id
        ):
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail="The payment was not found",
            )

        return payment_details


@router.post("/payments/{payment_id}/confirm")
@inject
def confirm_payment(
    payment_id: int,
    user: User = Depends(get_active_user),
    use_case: ConfirmPayment = Depends(Provide[Container.confirm_payment]),
) -> EmptyResponse:
    use_case(user=user, payment_id=payment_id)

    return EmptyResponse(success=True)


@router.post("/payments/{payment_id}/reject")
@inject
def reject_payment(
    payment_id: int,
    user: User = Depends(get_active_user),
    use_case: RejectPayment = Depends(Provide[Container.reject_payment]),
) -> EmptyResponse:
    use_case(user=user, payment_id=payment_id)

    return EmptyResponse(success=True)


@router.post("/payments/{payment_id}/cancel")
@inject
def cancel_payment(
    payment_id: int,
    user: User = Depends(get_active_user),
    use_case: CancelPayment = Depends(Provide[Container.cancel_payment]),
) -> EmptyResponse:
    use_case(user=user, payment_id=payment_id)

    return EmptyResponse(success=True)
