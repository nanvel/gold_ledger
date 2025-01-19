from dataclasses import dataclass
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import RetailerStoreTable
from app.models import RetailerStore, RetailerOrderBy, Timestamp


@dataclass(frozen=True)
class RetailStoreSearchItem:
    id: int
    name: str
    created_at: int


class RetailerStoresRepo:
    def __init__(self, session: Session):
        self._session = session

    def by_id(self, store_id: int) -> Optional[RetailerStore]:
        record = self._session.query(RetailerStoreTable).filter_by(id=store_id).first()
        if record:
            return RetailerStore(
                id=record.id,
                name=record.name,
                admin_id=record.admin_id,
            )

    def create(self, store: RetailerStore) -> int:
        supplier_store = RetailerStoreTable(
            name=store.name,
            admin_id=store.admin_id,
        )
        self._session.add(supplier_store)
        self._session.commit()

        self._session.refresh(supplier_store)

        return supplier_store.id

    def filter(
        self,
        q: Optional[str] = None,
        order_by: RetailerOrderBy = RetailerOrderBy.CREATED,
        reverse: bool = True,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[int, Tuple[RetailStoreSearchItem, ...]]:
        query = self._session.query(RetailerStoreTable)

        if q:
            query = query.filter(RetailerStoreTable.name.ilike(f"%{q}%"))

        total = query.count()

        if order_by == RetailerOrderBy.CREATED:
            order_field = RetailerStoreTable.created_at
        elif order_by == RetailerOrderBy.NANE:
            order_field = RetailerStoreTable.name
        else:
            raise ValueError(f"Unknown order_by value: {order_by}")

        if reverse:
            order_field = order_field.desc()

        records = query.order_by(order_field).offset(offset).limit(limit)

        return total, tuple(
            RetailStoreSearchItem(
                id=record.id,
                name=record.name,
                created_at=int(Timestamp.from_datetime(record.created_at)),
            )
            for record in records
        )
