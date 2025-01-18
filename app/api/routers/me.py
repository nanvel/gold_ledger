from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.container import Container
from app.models import StoreType, User
from app.repos.uow import UnitOfFork
from .auth import get_active_user

router = APIRouter()


class ResponseItem(BaseModel):
    id: int
    email: str
    role: int
    store_id: Optional[int]
    store_name: Optional[str]
    store_type: Optional[str]


@router.get("/me")
@inject
def get_me(
    user: User = Depends(get_active_user),
    uow: UnitOfFork = Depends(Provide[Container.uow]),
) -> ResponseItem:
    store_type = None
    print(user)
    if user.supplier_store_id is not None:
        store_type = StoreType.SUPPLIER
        with uow:
            store = uow.supplier_stores.by_id(user.supplier_store_id)
    elif user.retailer_store_id is not None:
        store_type = StoreType.RETAILER
        with uow:
            store = uow.retailer_stores.by_id(user.retailer_store_id)
    else:
        store = None

    if store:
        return ResponseItem(
            id=user.id,
            email=user.username,
            role=user.role.value,
            store_id=store.id,
            store_name=store.name,
            store_type=store_type.value,
        )

    return ResponseItem(
        id=user.id,
        email=user.username,
        role=user.role.value,
        store_id=None,
        store_name=None,
        store_type=None,
    )
