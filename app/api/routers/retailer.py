from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.container import Container
from app.models import User
from app.repos.uow import UnitOfFork
from .auth import get_active_user

router = APIRouter()


class ResponseItem(BaseModel):
    id: int
    name: str


@router.get("/retailers/{retailer_id}")
@inject
def get_retailer_info(
    retailer_id: int,
    user: User = Depends(get_active_user),
    uow: UnitOfFork = Depends(Provide[Container.uow]),
) -> ResponseItem:
    if not user.supplier_id:
        raise HTTPException(status_code=400, detail="Store is not a supplier.")

    with uow:
        retailer = uow.retailers.by_id(retailer_id)

    if not retailer:
        raise HTTPException(status_code=404, detail="Retailer not found.")

    return ResponseItem(id=retailer.id, name=retailer.name)
