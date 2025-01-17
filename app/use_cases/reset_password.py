from dataclasses import replace

from passlib.context import CryptContext

from app.repos.uow import UnitOfFork


class ResetPassword:
    def __init__(self, uow: UnitOfFork, crypt_context: CryptContext):
        self._uow = uow
        self._crypt_context = crypt_context

    def __call__(self, username: str, password: str):
        with self._uow:
            user = self._uow.users.by_username(username)
            if not user:
                return
            user = replace(user, password_hash=self._crypt_context.hash(password))
            self._uow.users.update(user)
            return self._uow.users.by_id(user.id)
