from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.container import Container
from app.models import User
from app.repos.uow import UnitOfWork
from .auth import get_active_user

router = APIRouter()


class ConnectForm(BaseModel):
    code: str


class ResponseItem(BaseModel):
    success: bool


@router.post("/connect")
@inject
def connect(
    item: ConnectForm,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> ResponseItem:
    with uow:
        invite = uow.invites.get(item.code)

        if invite is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[
                    {
                        "type": "invalid_code",
                        "loc": ["body", "code"],
                        "msg": "Code is invalid",
                        "input": item.code,
                        "ctx": {},
                    }
                ],
            )

        if user.supplier_id:
            supplier_id = user.supplier_id
            retailer_id = invite.retailer_id
        else:
            supplier_id = invite.supplier_id
            retailer_id = user.retailer_id

        if not supplier_id or not retailer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=[
                    {
                        "type": "invalid_code",
                        "loc": ["body", "code"],
                        "msg": "Can only be applied by a {}".format(
                            "retailer" if invite.supplier_id else "supplier"
                        ),
                        "input": item.code,
                        "ctx": {},
                    }
                ],
            )

        connection = uow.connections.get(
            supplier_id=supplier_id,
            retailer_id=retailer_id,
        )
        if connection:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=[
                    {
                        "type": "invalid_code",
                        "loc": ["body", "code"],
                        "msg": "Already connected",
                        "input": item.code,
                        "ctx": {},
                    }
                ],
            )

        uow.connections.create(supplier_id=supplier_id, retailer_id=retailer_id)
        uow.invites.apply(item.code)

    return ResponseItem(success=True)


class InviteResponseItem(BaseModel):
    code: str


@router.get("/connect")
@inject
def get_invite(
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
) -> InviteResponseItem:
    with uow:
        invite = uow.invites.create(
            supplier_id=user.supplier_id,
            retailer_id=user.retailer_id,
        )

    return InviteResponseItem(code=invite.code)
