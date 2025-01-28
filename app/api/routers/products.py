from dataclasses import replace
from datetime import date
from decimal import Decimal
from typing import Optional, Tuple

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.container import Container
from app.models import Activity, ActivityType, Product, User
from app.repos.products import ProductDetailsItem, ProductSearchItem
from app.repos.uow import UnitOfWork
from .auth import get_active_user

router = APIRouter()


class ProductForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    date: date
    weight: Decimal = Field(..., gt=0)
    quality: Decimal = Field(..., ge=0, le=100)
    rate_per_gram: Decimal = Field(..., gt=0)
    total_amount: Decimal = Field(..., gt=0)
    payment_due_date: date
    retailer_id: int
    image_id: Optional[int]


class ProductResponse(BaseModel):
    success: bool


@router.post("/products", status_code=201)
@inject
def create_product(
    item: ProductForm,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    activity_message_factory=Depends(Provide[Container.activity_message_factory]),
) -> ProductResponse:
    if not user.is_supplier:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user is not a supplier.",
        )

    with uow:
        retailer = uow.retailers.by_id(item.retailer_id)

        if retailer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The retailer store was not found.",
            )

        if item.image_id:
            image = uow.images.by_id(item.image_id)

            if image is None or not image.supplier_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The image was not found.",
                )

            if image.supplier_id != user.supplier_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The image does not belong to the store.",
                )
        else:
            image = None

        product = Product(
            id=0,
            name=item.name,
            date=item.date,
            weight=item.weight,
            quality=item.quality,
            rate_per_gram=item.rate_per_gram,
            total_amount=item.total_amount,
            payment_due_date=item.payment_due_date,
            custom_fields={},
            supplier_id=user.supplier_id,
            retailer_id=retailer.id,
            creator_id=user.id,
            confirmed_by=None,
            rejected_by=None,
        )
        product_id = uow.products.create(product)
        product = replace(product, id=product_id)

        if image:
            uow.products.add_image(product, image)

        activity = Activity(
            id=0,
            type=ActivityType.PRODUCT_GIVEN,
            user_id=user.id,
            supplier_id=user.supplier_id,
            retailer_id=retailer.id,
            product_id=product_id,
            payment_id=None,
            message="",
        )
        activity = replace(
            activity,
            message=activity_message_factory.from_activity(activity, uow=uow),
        )
        uow.activities.create(activity)

    return ProductResponse(success=True)


class ProductsResponse(BaseModel):
    total: int
    items: Tuple[ProductSearchItem, ...]


@router.get("/products")
@inject
def get_products(
    retailer_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
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
) -> ProductDetailsItem:
    with uow:
        product_details = uow.products.details(product_id)

        if not product_details or (
            product_details.supplier_id != user.supplier_id
            and product_details.retailer_id != user.retailer_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The product was not found.",
            )

        return product_details


class UpdateResponse(BaseModel):
    success: bool


@router.post("/products/{product_id}/confirm")
@inject
def confirm_product(
    product_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    activity_message_factory=Depends(Provide[Container.activity_message_factory]),
) -> UpdateResponse:
    with uow:
        product = uow.products.by_id(product_id)

        if not product or product.retailer_id != user.retailer_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The product was not found.",
            )

        assert product.rejected_by is None
        assert product.confirmed_by is None

        product = replace(product, confirmed_by=user.id)

        uow.products.update(product)

        activity = Activity(
            id=0,
            type=ActivityType.PRODUCT_CONFIRMED,
            user_id=user.id,
            supplier_id=user.supplier_id,
            retailer_id=user.retailer_id,
            product_id=product_id,
            payment_id=None,
            message="",
        )
        activity = replace(
            activity,
            message=activity_message_factory.from_activity(activity, uow=uow),
        )
        uow.activities.create(activity)

    return UpdateResponse(success=True)


@router.post("/products/{product_id}/reject")
@inject
def reject_product(
    product_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    activity_message_factory=Depends(Provide[Container.activity_message_factory]),
) -> UpdateResponse:
    with uow:
        product = uow.products.by_id(product_id)

        if not product or product.retailer_id != user.retailer_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The product was not found.",
            )

        assert product.rejected_by is None
        assert product.confirmed_by is None

        product = replace(product, rejected_by=user.id)

        uow.products.update(product)

        activity = Activity(
            id=0,
            type=ActivityType.PRODUCT_REJECTED,
            user_id=user.id,
            supplier_id=user.supplier_id,
            retailer_id=user.retailer_id,
            product_id=product_id,
            payment_id=None,
            message="",
        )
        activity = replace(
            activity,
            message=activity_message_factory.from_activity(activity, uow=uow),
        )
        uow.activities.create(activity)

    return UpdateResponse(success=True)
