from typing import Optional, Tuple

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.container import Container
from app.models import RetailerOrderBy, User
from app.repos.uow import UnitOfWork
from app.repos.retailers import RetailerSearchItem
from .auth import get_active_user

router = APIRouter()


class ResponseItem(BaseModel):
    items: Tuple[RetailerSearchItem, ...]
    total: int


@router.get("/retailers")
@inject
def filter_retailers(
    q: Optional[str] = None,
    offset: int = 0,
    limit: int = 20,
    order_by: RetailerOrderBy = RetailerOrderBy.CREATED,
    reverse: bool = True,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> ResponseItem:
    with uow:
        total, items = uow.retailers.filter(
            supplier_id=user.supplier_id,
            q=q,
            order_by=order_by,
            reverse=reverse,
            offset=offset,
            limit=limit,
        )

    return ResponseItem(items=items, total=total)
