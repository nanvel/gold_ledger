from dataclasses import replace
from http.client import HTTPException
from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.container import Container
from app.models import User
from app.repos.uow import UnitOfWork
from .auth import get_active_user

router = APIRouter()


class ResponseItem(BaseModel):
    id: int
    email: str
    name: Optional[str]
    supplier_id: Optional[int]
    retailer_id: Optional[int]
    store_name: Optional[str]
    store_owner_id: Optional[int]


@router.get("/me")
@inject
def get_me(
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> ResponseItem:
    if user.supplier_id is not None:
        with uow:
            store = uow.suppliers.by_id(user.supplier_id)
    elif user.retailer_id is not None:
        with uow:
            store = uow.retailers.by_id(user.retailer_id)
    else:
        store = None

    return ResponseItem(
        id=user.id,
        email=user.username,
        name=user.name,
        store_name=store and store.name or None,
        supplier_id=user.supplier_id,
        retailer_id=user.retailer_id,
        store_owner_id=store and store.owner_id or None,
    )


class ChangeNameForm(BaseModel):
    name: str = Field(..., max_length=64)


class ChangeNameResponse(BaseModel):
    success: bool


@router.put("/me/name")
@inject
def set_name(
    item: ChangeNameForm,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> ChangeNameResponse:
    with uow:
        user = replace(user, name=item.name)
        uow.users.update(user)

    return ChangeNameResponse(success=True)


class ChangeStoreNameForm(BaseModel):
    name: str = Field(..., min_length=2, max_length=64)


@router.put("/me/store-name")
@inject
def set_store_name(
    item: ChangeStoreNameForm,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> ChangeNameResponse:
    with uow:
        if user.supplier_id is not None:
            supplier = uow.suppliers.by_id(user.supplier_id)
            if supplier.owner_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No permission to change store name",
                )

            supplier = replace(supplier, name=item.name)
            uow.suppliers.update(supplier)
        elif user.retailer_id is not None:
            retailer = uow.retailers.by_id(user.retailer_id)

            if retailer.owner_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No permission to change store name",
                )

            retailer = replace(retailer, name=item.name)
            uow.retailers.update(retailer)

    return ChangeNameResponse(success=True)
