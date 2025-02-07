from datetime import date
from decimal import Decimal
from typing import Optional, Tuple

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.container import Container
from app.models import DisplayProduct, PaymentType, ProductStatus, User
from app.repos.uow import UnitOfWork
from app.use_cases.add_product import AddProduct
from app.use_cases.cancel_product import CancelProduct
from app.use_cases.confirm_product import ConfirmProduct
from app.use_cases.reject_product import RejectProduct
from .auth import get_active_user

router = APIRouter()


class ProductForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    date: date
    weight: Decimal = Field(..., gt=0)
    quality: Decimal = Field(..., gt=0, le=100)
    rate: Decimal = Field(..., gt=0)
    payment_type: PaymentType
    payment_amount: Optional[Decimal] = Field(None, gt=0)
    payment_quality: Optional[Decimal] = Field(None, gt=0, le=100)
    payment_weight: Optional[Decimal] = Field(None, gt=0)
    payment_due_date: date
    retailer_id: int
    image_id: Optional[int]


class EmptyResponse(BaseModel):
    success: bool


@router.post("/products", status_code=201)
@inject
def add_product(
    item: ProductForm,
    user: User = Depends(get_active_user),
    use_case: AddProduct = Depends(Provide[Container.add_product]),
) -> EmptyResponse:
    if not user.is_supplier:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user is not a supplier",
        )

    if item.payment_type == PaymentType.FINE:
        if item.payment_quality is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "type": "payment_quality_required",
                        "loc": ["body", "payment_quality"],
                        "msg": "Payment quality is required for fine payment",
                        "input": item.payment_quality,
                        "ctx": {},
                    }
                ],
            )
        elif item.payment_weight is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "type": "payment_weight_required",
                        "loc": ["body", "payment_weight"],
                        "msg": "Payment weight is required for fine payment",
                        "input": item.payment_weight,
                        "ctx": {},
                    }
                ],
            )
    else:
        if item.payment_amount is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "type": "payment_amount_required",
                        "loc": ["body", "payment_amount"],
                        "msg": "Payment amount is required for cash payment",
                        "input": item.payment_amount,
                        "ctx": {},
                    }
                ],
            )

    if item.payment_due_date < item.date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "type": "payment_due_date_invalid",
                    "loc": ["body", "payment_due_date"],
                    "msg": "Due date must be greater than the date or equal",
                    "input": item.payment_due_date.isoformat(),
                    "ctx": {},
                }
            ],
        )

    use_case(
        retailer_id=item.retailer_id,
        supplier_id=user.supplier_id,
        creator_id=user.id,
        name=item.name,
        date_=item.date,
        weight=item.weight,
        quality=item.quality,
        rate=item.rate,
        payment_type=item.payment_type,
        payment_amount=item.payment_amount,
        payment_weight=item.payment_weight,
        payment_quality=item.payment_quality,
        payment_due_date=item.payment_due_date,
        image_id=item.image_id,
    )

    return EmptyResponse(success=True)


class ProductsResponse(BaseModel):
    total: int
    items: Tuple[DisplayProduct, ...]


@router.get("/products")
@inject
def get_products(
    retailer_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    status: Optional[ProductStatus] = None,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    limit: int = 20,
    offset: int = 0,
) -> ProductsResponse:
    if user.is_supplier:
        supplier_id = user.supplier_id
    else:
        retailer_id = user.retailer_id

    with uow:
        total, items = uow.products.filter(
            supplier_id=supplier_id,
            retailer_id=retailer_id,
            status=status,
            limit=limit,
            offset=offset,
        )

    return ProductsResponse(total=total, items=items)


@router.get("/products/{product_id}")
@inject
def get_product(
    product_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> DisplayProduct:
    with uow:
        product_details = uow.products.display(product_id)

        if not product_details or (
            product_details.supplier.id != user.supplier_id
            and product_details.retailer.id != user.retailer_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The product was not found",
            )

        return product_details


@router.post("/products/{product_id}/confirm")
@inject
def confirm_product(
    product_id: int,
    user: User = Depends(get_active_user),
    use_case: ConfirmProduct = Depends(Provide[Container.confirm_product]),
) -> EmptyResponse:
    use_case(user=user, product_id=product_id)

    return EmptyResponse(success=True)


@router.post("/products/{product_id}/reject")
@inject
def reject_product(
    product_id: int,
    user: User = Depends(get_active_user),
    use_case: RejectProduct = Depends(Provide[Container.reject_product]),
) -> EmptyResponse:
    use_case(user=user, product_id=product_id)

    return EmptyResponse(success=True)


@router.post("/products/{product_id}/cancel")
@inject
def cancel_product(
    product_id: int,
    user: User = Depends(get_active_user),
    user_case: CancelProduct = Depends(Provide[Container.cancel_product]),
) -> EmptyResponse:
    user_case(user=user, product_id=product_id)

    return EmptyResponse(success=True)
