from decimal import Decimal

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.container import Container
from app.models import Product, Timestamp, User
from app.repos.uow import UnitOfFork
from .auth import get_active_user

router = APIRouter()


class ProductForm(BaseModel):
    name: str
    date: int
    weight: str
    quality: str
    rate_per_gram: str
    total_amount: str
    retailer_id: int


class ProductResponse(BaseModel):
    success: bool


@router.post("/products", status_code=201)
@inject
def create_product(
    item: ProductForm,
    user: User = Depends(get_active_user),
    uow: UnitOfFork = Depends(Provide[Container.uow]),
) -> ProductResponse:
    with uow:
        retailer = uow.retailer_stores.by_id(item.retailer_store_id)

        if retailer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The retailer store was not found.",
            )

        uow.products.create(
            Product(
                id=0,
                name=item.name,
                date=Timestamp(item.date),
                weight=Decimal(item.weight),
                quality=Decimal(item.quality),
                rate_per_gram=Decimal(item.rate_per_gram),
                total_amount=Decimal(item.total_amount),
                custom_fields={},
                picture={},
                supplier_id=user.supplier_store_id,
                retailer_id=item.retailer.id,
                creator_id=user.id,
            )
        )

    return ProductResponse(success=True)
