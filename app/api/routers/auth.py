from pydantic import BaseModel, EmailStr
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.container import Container
from app.models import User, UserRole
from app.repos.users import UsersRepo

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: UserRole


@router.post("/token", response_model=TokenResponse)
@inject
def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    users_repo: UsersRepo = Depends(Provide[Container.users_repo]),
    crypt_context: CryptContext = Depends(Provide[Container.crypt_context]),
    secret_key: str = Depends(Provide[Container.config.secret_key]),
    jwt_algorithm: str = Depends(Provide[Container.jwt_algorithm]),
) -> TokenResponse:
    user = users_repo.by_username(form_data.username)

    if user and crypt_context.verify(form_data.password, user.password_hash):
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
            role=user.role,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User authentication failed.",
    )


class RegistrationItem(BaseModel):
    email: EmailStr


@inject
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    users_repo: UsersRepo = Depends(Provide[Container.users_repo]),
    secret_key: str = Depends(Provide[Container.config.secret_key]),
    jwt_algorithm: str = Depends(Provide[Container.jwt_algorithm]),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[jwt_algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        token_version: int = payload.get("v")
        if username is None or user_id is None or token_version is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = users_repo.by_id(user_id)
    if user is None or user.token_version != token_version:
        raise credentials_exception

    return user


def get_active_user(user: Annotated[User, Depends(get_current_user)]):
    return user


def get_employee_user(user: Annotated[User, Depends(get_current_user)]):
    if user.role in {UserRole.ADMIN, UserRole.EMPLOYEE}:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User does not have enough privileges.",
    )


def get_admin_user(user: Annotated[User, Depends(get_current_user)]):
    if user.role == UserRole.ADMIN:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User does not have enough privileges.",
    )
