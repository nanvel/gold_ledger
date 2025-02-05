import pytz

from datetime import datetime
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.container import Container
from app.models import User
from app.repos.uow import UnitOfWork
from app.services.accounting import AccountingService
from .auth import get_active_user

router = APIRouter()


@router.get("/accounting")
@inject
def get_accounting(
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
):
    india_tz = pytz.timezone("Asia/Kolkata")
    india_date = datetime.now(india_tz).date()

    with uow:
        if user.supplier_id:
            res = Accounting(uow._session).for_supplier(
                user.supplier_id,
                today=india_date,
            )
        else:
            res = Accounting(uow._session).for_retailer(
                user.retailer_id,
                today=india_date,
            )

    for k, v in res.items():
        v["id"] = k

    res = sorted(res.values(), key=lambda x: x["id"])

    return res
