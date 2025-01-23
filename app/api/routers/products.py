from dataclasses import replace
from decimal import Decimal
from typing import Optional, Tuple

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.container import Container
from app.models import Product, Timestamp, User
from app.repos.products import ProductSearchItem
from app.repos.uow import UnitOfFork
from .auth import get_active_user

router = APIRouter()


class ProductForm(BaseModel):
    name: str
    date: str
    weight: Decimal
    quality: Decimal
    rate_per_gram: Decimal
    total_amount: Decimal
    retailer_id: int
    image_id: Optional[int]


class ProductResponse(BaseModel):
    success: bool


@router.post("/products", status_code=201)
@inject
def create_product(
    item: ProductForm,
    user: User = Depends(get_active_user),
    uow: UnitOfFork = Depends(Provide[Container.uow]),
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
            date=Timestamp.from_string(item.date),
            weight=item.weight,
            quality=item.quality,
            rate_per_gram=item.rate_per_gram,
            total_amount=item.total_amount,
            custom_fields={},
            supplier_id=user.supplier_id,
            retailer_id=retailer.id,
            creator_id=user.id,
        )
        product_id = uow.products.create(product)
        product = replace(product, id=product_id)

        if image:
            uow.products.add_image(product, image)

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
    uow: UnitOfFork = Depends(Provide[Container.uow]),
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
