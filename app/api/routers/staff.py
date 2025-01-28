from typing import Tuple

from dependency_injector.wiring import Provide, inject
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from app.container import Container
from app.models import User
from app.repos.uow import UnitOfWork
from app.repos.users import UsersSearchItems
from .auth import get_active_user

router = APIRouter()


class AddStaffForm(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class StoreResponse(BaseModel):
    success: bool


@router.post("/staff", status_code=201)
@inject
def add_staff(
    item: AddStaffForm,
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    crypt_context: CryptContext = Depends(Provide[Container.crypt_context]),
) -> StoreResponse:
    with uow:
        if user.supplier_id:
            store = uow.suppliers.by_id(user.supplier_id)
        elif user.retailer_id:
            store = uow.retailers.by_id(user.retailer_id)

        if store.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )

        staff = uow.users.by_username(str(item.email))

        if staff is not None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "type": "user_exists",
                        "loc": ["body", "email"],
                        "msg": "The email was already registered",
                        "input": item.email,
                        "ctx": {},
                    }
                ],
            )

        uow.users.create(
            User(
                id=0,
                username=str(item.email),
                password_hash=crypt_context.hash(item.password),
                token_version=0,
                supplier_id=user.supplier_id,
                retailer_id=user.retailer_id,
            )
        )

    return StoreResponse(success=True)


class ListStaffResponse(BaseModel):
    items: Tuple[UsersSearchItems, ...]
    total: int


@router.get("/staff", status_code=200)
@inject
def list_staff(
    user: User = Depends(get_active_user),
    uow: UnitOfWork = Depends(Provide[Container.uow]),
    limit: int = 20,
    offset: int = 0,
) -> ListStaffResponse:
    with uow:
        if user.supplier_id:
            store = uow.suppliers.by_id(user.supplier_id)
        elif user.retailer_id:
            store = uow.retailers.by_id(user.retailer_id)

        if store.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )

        total, staff = uow.users.filter(
            supplier_id=user.supplier_id,
            retailer_id=user.retailer_id,
            limit=limit,
            offset=offset,
        )

    return ListStaffResponse(total=total, items=staff)
