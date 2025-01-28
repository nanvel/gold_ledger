from typing import Optional, Tuple

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.container import Container
from app.models import SupplierOrderBy
from app.repos.suppliers import SupplierSearchItem
from app.repos.uow import UnitOfWork
from .auth import get_active_user

router = APIRouter()


class ResponseItem(BaseModel):
    items: Tuple[SupplierSearchItem, ...]
    total: int


@router.get("/suppliers", dependencies=[Depends(get_active_user)])
@inject
def filter_suppliers(
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    q: Optional[str] = None,
    offset: int = 0,
    limit: int = 20,
    order_by: SupplierOrderBy = SupplierOrderBy.CREATED,
    reverse: bool = True,
) -> ResponseItem:
    with uow:
        total, items = uow.suppliers.filter(
            q=q,
            order_by=order_by,
            reverse=reverse,
            offset=offset,
            limit=limit,
        )

    return ResponseItem(items=items, total=total)
