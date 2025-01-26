from typing import Optional

from sqlalchemy.orm import Session

from app.db import SupplierTable
from app.models import Supplier


class SuppliersRepo:
    def __init__(self, session: Session):
        self._session = session

    def by_id(self, supplier_id: int) -> Optional[Supplier]:
        record = self._session.query(SupplierTable).filter_by(id=supplier_id).first()
        if record:
            return Supplier(
                id=record.id,
                name=record.name,
                owner_id=record.owner_id,
            )

    def create(self, supplier: Supplier) -> int:
        record = SupplierTable(
            name=supplier.name,
            owner_id=supplier.owner_id,
        )
        self._session.add(record)
        self._session.commit()

        self._session.refresh(record)

        return record.id

    def update(self, supplier: Supplier):
        record = self._session.query(SupplierTable).filter_by(id=supplier.id).first()
        if record:
            record.name = supplier.name
            self._session.commit()
