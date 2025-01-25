from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.container import Container
from app.models import User
from app.repos.uow import UnitOfFork
from .auth import get_active_user

router = APIRouter()


class ResponseItem(BaseModel):
    id: int
    email: str
    supplier_id: Optional[int]
    retailer_id: Optional[int]
    store_name: Optional[str]
    store_owner_id: Optional[int]


@router.get("/me")
@inject
def get_me(
    user: User = Depends(get_active_user),
    uow: UnitOfFork = Depends(Provide[Container.uow]),
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
        store_name=store and store.name or None,
        supplier_id=user.supplier_id,
        retailer_id=user.retailer_id,
        store_owner_id=store and store.owner_id or None,
    )
