from typing import Optional, Tuple

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.container import Container
from app.models import User
from app.repos.activities import ActivitySearchItem
from app.repos.uow import UnitOfWork
from .auth import get_active_user

router = APIRouter()


class ResponseItem(BaseModel):
    items: Tuple[ActivitySearchItem, ...]
    total: int


@router.get("/activities")
@inject
def filter_activities(
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    retailer_id: Optional[int] = None,
    supplier_id: Optional[int] = None,
    product_id: Optional[int] = None,
    payment_id: Optional[int] = None,
    offset: int = 0,
    limit: int = 20,
) -> ResponseItem:
    if user.retailer_id is not None:
        retailer_id = user.retailer_id
    if user.supplier_id is not None:
        supplier_id = user.supplier_id

    with uow:
        total, items = uow.activities.filter(
            retailer_id=retailer_id,
            supplier_id=supplier_id,
            product_id=product_id,
            payment_id=payment_id,
            offset=offset,
            limit=limit,
        )

    return ResponseItem(items=items, total=total)
