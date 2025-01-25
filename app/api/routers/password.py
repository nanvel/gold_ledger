from dataclasses import replace
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from app.container import Container
from app.models import User
from app.repos.uow import UnitOfFork
from .auth import get_active_user


router = APIRouter()


class ChangePasswordForm(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)


class Response(BaseModel):
    success: bool


@router.post("/change-password", status_code=200)
@inject
def change_password(
    item: ChangePasswordForm,
    user: User = Depends(get_active_user),
    uow: UnitOfFork = Depends(Provide[Container.uow]),
    crypt_context: CryptContext = Depends(Provide[Container.crypt_context]),
) -> Response:
    if not crypt_context.verify(item.old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "type": "invalid_password",
                    "loc": ["body", "old_password"],
                    "msg": "Old password is incorrect",
                    "input": item.old_password,
                    "ctx": {},
                }
            ],
        )

    with uow:
        user = replace(user, password_hash=crypt_context.hash(item.new_password))
        uow.users.update(user)

    return Response(success=True)
