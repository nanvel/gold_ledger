from dataclasses import replace
from dependency_injector.wiring import Provide, inject
from jose import jwt
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel

from app.container import Container
from app.models import RetailerStore, StoreType, SupplierStore, User, UserRole
from app.repos.uow import UnitOfFork
from .auth import TokenResponse

router = APIRouter()


class RegisterStoreForm(BaseModel):
    type: str
    name: str
    email: EmailStr
    password: str


@router.post("/register", response_model=TokenResponse)
@inject
def register_store(
    item: RegisterStoreForm,
    uow: UnitOfFork = Depends(Provide[Container.uow]),
    crypt_context: CryptContext = Depends(Provide[Container.crypt_context]),
    secret_key: str = Depends(Provide[Container.config.secret_key]),
    jwt_algorithm: str = Depends(Provide[Container.jwt_algorithm]),
) -> TokenResponse:
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
                role=UserRole.SHOP_OWNER,
                token_version=0,
                supplier_store_id=None,
                retailer_store_id=None,
            )
        )
        user = uow.users.by_id(user_id)

        if item.type == StoreType.SUPPLIER:
            store = SupplierStore(id=0, name=item.name, admin_id=admin.id)
            store_id = uow.supplier_stores.create(store)
            user = replace(user, supplier_store_id=store_id)
        elif item.type == StoreType.RETAILER:
            store = RetailerStore(id=0, name=item.name, admin_id=admin.id)
            store_id = uow.retailer_stores.create(store)
            user = replace(user, retailer_store_id=store_id)

        uow.users.update(user)

    return TokenResponse(
        access_token=jwt.encode(
            {
                "sub": user.username,
                "id": user.id,
                "v": user.token_version,
            },
            secret_key,
            algorithm=jwt_algorithm,
        ),
        token_type="bearer",
        role=user.role.value,
    )
