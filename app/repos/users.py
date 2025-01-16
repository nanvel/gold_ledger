from typing import Optional

from sqlalchemy.orm import Session

from app.db import UserTable
from app.models import User, UserRole


class UsersRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, user: User):
        record = UserTable(
            username=user.username,
            password_hash=user.password_hash,
            role=user.role.value,
        )

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return record.id

    def by_id(self, user_id: int) -> Optional[User]:
        record = self._session.query(UserTable).where(UserTable.id == user_id).first()
        if record:
            return User(
                id=record.id,
                username=record.username,
                password_hash=record.password_hash,
                role=UserRole(record.role),
                token_version=record.token_version,
            )

    def by_username(self, username: str) -> Optional[User]:
        record = (
            self._session.query(UserTable).where(UserTable.username == username).first()
        )
        if record:
            return User(
                id=record.id,
                username=record.username,
                password_hash=record.password_hash,
                role=UserRole(record.role),
                token_version=record.token_version,
            )
