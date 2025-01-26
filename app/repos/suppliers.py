import re
from dataclasses import dataclass
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import SupplierTable
from app.models import Supplier, SupplierOrderBy, Timestamp

STORE_ID_RE = re.compile(r"^\d+$")


@dataclass(frozen=True)
class SupplierSearchItem:
    id: int
    name: str
    created_at: int


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

    def filter(
        self,
        q: Optional[str] = None,
        order_by: SupplierOrderBy = SupplierOrderBy.CREATED,
        reverse: bool = True,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[int, Tuple[SupplierSearchItem, ...]]:
        query = self._session.query(SupplierTable)

        if q:
            q = q.strip()
            if STORE_ID_RE.match(q):
                query = query.filter(SupplierTable.id == int(q))
            else:
                query = query.filter(SupplierTable.name.ilike(f"%{q}%"))

        total = query.count()

        if order_by == SupplierOrderBy.CREATED:
            order_field = SupplierTable.created_at
        elif order_by == SupplierOrderBy.NANE:
            order_field = SupplierTable.name
        else:
            raise ValueError(f"Unknown order_by value: {order_by}")

        if reverse:
            order_field = order_field.desc()

        records = query.order_by(order_field).offset(offset).limit(limit)

        return total, tuple(
            SupplierSearchItem(
                id=record.id,
                name=record.name,
                created_at=int(Timestamp.from_datetime(record.created_at)),
            )
            for record in records
        )
