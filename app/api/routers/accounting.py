from dataclasses import dataclass
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.container import Container
from app.models import DisplayCache, User
from app.repos.uow import UnitOfWork
from .auth import get_active_user

router = APIRouter()


@dataclass(frozen=True)
class AccountingResponse:
    items: List[DisplayCache]


@router.get("/accounting")
@inject
def get_accounting(
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> AccountingResponse:
    with uow:
        res = uow.cache.filter(
            supplier_id=user.supplier_id, retailer_id=user.retailer_id
        )

    return AccountingResponse(items=res)
