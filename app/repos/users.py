from dataclasses import dataclass
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import UserTable
from app.models import User


@dataclass(frozen=True)
class UsersSearchItems:
    id: int
    email: str
    name: str
    created_at: int


class UsersRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, user: User):
        record = UserTable(
            username=user.username,
            password_hash=user.password_hash,
            supplier_id=user.supplier_id,
            retailer_id=user.retailer_id,
            name=user.name,
        )

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return record.id

    def update(self, user: User):
        record = self._session.query(UserTable).where(UserTable.id == user.id).first()
        if record:
            record.username = user.username
            record.password_hash = user.password_hash
            record.token_version = user.token_version
            record.supplier_id = user.supplier_id
            record.retailer_id = user.retailer_id
            record.name = user.name

            self._session.commit()

    def by_id(self, user_id: int) -> Optional[User]:
        record = self._session.query(UserTable).where(UserTable.id == user_id).first()
        if record:
            return User(
                id=record.id,
                username=record.username,
                password_hash=record.password_hash,
                token_version=record.token_version,
                supplier_id=record.supplier_id,
                retailer_id=record.retailer_id,
                name=record.name,
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
                token_version=record.token_version,
                supplier_id=record.supplier_id,
                retailer_id=record.retailer_id,
                name=record.name,
            )

    def filter(
        self,
        supplier_id: Optional[int],
        retailer_id: Optional[int],
        limit: int,
        offset: int,
    ) -> Tuple[int, Tuple[UsersSearchItems, ...]]:
        query = self._session.query(UserTable)

        if supplier_id:
            query = query.filter(UserTable.supplier_id == supplier_id)
        if retailer_id:
            query = query.filter(UserTable.retailer_id == retailer_id)

        total = query.count()

        records = (
            query.order_by(UserTable.created_at.desc()).offset(offset).limit(limit)
        )

        return total, tuple(
            UsersSearchItems(
                id=record.id,
                email=record.username,
                name=record.name,
                created_at=int(record.created_at.timestamp()),
            )
            for record in records
        )
