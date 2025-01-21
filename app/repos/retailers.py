from dataclasses import dataclass
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import RetailerTable
from app.models import Retailer, RetailerOrderBy, Timestamp


@dataclass(frozen=True)
class RetailerSearchItem:
    id: int
    name: str
    created_at: int


class RetailersRepo:
    def __init__(self, session: Session):
        self._session = session

    def by_id(self, retailer_id: int) -> Optional[Retailer]:
        record = self._session.query(RetailerTable).filter_by(id=retailer_id).first()
        if record:
            return Retailer(
                id=record.id,
                name=record.name,
                admin_id=record.admin_id,
            )

    def create(self, retailer: Retailer) -> int:
        record = RetailerTable(
            name=retailer.name,
            admin_id=retailer.admin_id,
        )
        self._session.add(record)
        self._session.commit()

        self._session.refresh(record)

        return record.id

    def filter(
        self,
        q: Optional[str] = None,
        order_by: RetailerOrderBy = RetailerOrderBy.CREATED,
        reverse: bool = True,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[int, Tuple[RetailerSearchItem, ...]]:
        query = self._session.query(RetailerTable)

        if q:
            query = query.filter(RetailerTable.name.ilike(f"%{q}%"))

        total = query.count()

        if order_by == RetailerOrderBy.CREATED:
            order_field = RetailerTable.created_at
        elif order_by == RetailerOrderBy.NANE:
            order_field = RetailerTable.name
        else:
            raise ValueError(f"Unknown order_by value: {order_by}")

        if reverse:
            order_field = order_field.desc()

        records = query.order_by(order_field).offset(offset).limit(limit)

        return total, tuple(
            RetailerSearchItem(
                id=record.id,
                name=record.name,
                created_at=int(Timestamp.from_datetime(record.created_at)),
            )
            for record in records
        )
