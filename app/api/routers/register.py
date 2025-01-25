from dataclasses import replace
from dependency_injector.wiring import Provide, inject
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel

from app.container import Container
from app.models import Retailer, StoreType, Supplier, User
from app.repos.uow import UnitOfFork

router = APIRouter()


class RegisterStoreForm(BaseModel):
    type: StoreType
    name: str
    email: EmailStr
    password: str


class StoreResponse(BaseModel):
    success: bool


@router.post("/register", status_code=201)
@inject
def register_store(
    item: RegisterStoreForm,
    uow: UnitOfFork = Depends(Provide[Container.uow]),
    crypt_context: CryptContext = Depends(Provide[Container.crypt_context]),
) -> StoreResponse:
    with uow:
        user = uow.users.by_username(str(item.email))

        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The email was already registered.",
            )

        user_id = uow.users.create(
            User(
                id=0,
                username=str(item.email),
                password_hash=crypt_context.hash(item.password),
                token_version=0,
                supplier_id=None,
                retailer_id=None,
            )
        )
        user = uow.users.by_id(user_id)

        if item.type == StoreType.SUPPLIER:
            store = Supplier(id=0, name=item.name, owner_id=user.id)
            store_id = uow.suppliers.create(store)
            user = replace(user, supplier_store_id=store_id)
        elif item.type == StoreType.RETAILER:
            store = Retailer(id=0, name=item.name, owner_id=user.id)
            store_id = uow.retailers.create(store)
            user = replace(user, retailer_store_id=store_id)

        uow.users.update(user)

    return StoreResponse(success=True)
