from passlib.context import CryptContext

from app.models import User, UserRole
from app.repos.uow import UnitOfFork


class CreateUser:
    def __init__(self, uow: UnitOfFork, crypt_context: CryptContext):
        self._uow = uow
        self._crypt_context = crypt_context

    def __call__(self, username: str, password: str, role: int) -> User:
        user = User(
            id=0,
            username=username,
            password_hash=self._crypt_context.hash(password),
            role=UserRole(role),
            token_version=0,
        )
        with self._uow:
            user_id = self._uow.users.create(user)
            return self._uow.users.by_id(user_id)
