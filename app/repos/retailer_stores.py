from typing import Optional

from sqlalchemy.orm import Session

from app.db import RetailerStoreTable
from app.models import RetailerStore


class RetailerStoresRepo:
    def __init__(self, session: Session):
        self._session = session

    def by_id(self, store_id: int) -> Optional[RetailerStore]:
        record = self._session.query(RetailerStoreTable).filter_by(id=store_id)
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
