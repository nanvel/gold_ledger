from typing import Optional

from sqlalchemy.orm import Session

from app.db import SupplierStoreTable
from app.models import SupplierStore


class SupplierStoresRepo:
    def __init__(self, session: Session):
        self._session = session

    def by_id(self, store_id: int) -> Optional[SupplierStore]:
        record = self._session.query(SupplierStoreTable).filter_by(id=store_id)
        if record:
            return SupplierStore(
                id=record.id,
                name=record.name,
                admin_id=record.admin_id,
            )

    def create(self, store: SupplierStore) -> int:
        supplier_store = SupplierStoreTable(
            name=store.name,
            admin_id=store.admin_id,
        )
        self._session.add(supplier_store)
        self._session.commit()

        self._session.refresh(supplier_store)

        return supplier_store.id
