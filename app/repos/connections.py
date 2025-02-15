from typing import Optional

from sqlalchemy.orm import Session

from app.db import ConnectionTable


class ConnectionsRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, supplier_id: int, retailer_id: int):
        record = (
            self._session.query(ConnectionTable)
            .filter(
                ConnectionTable.supplier_id == supplier_id,
                ConnectionTable.retailer_id == retailer_id,
            )
            .first()
        )

        if not record:
            record = ConnectionTable(
                supplier_id=supplier_id,
                retailer_id=retailer_id,
            )
            self._session.add(record)
            self._session.commit()

    def get(self, supplier_id: int, retailer_id: int) -> Optional[int]:
        record = (
            self._session.query(ConnectionTable)
            .filter(
                ConnectionTable.supplier_id == supplier_id,
                ConnectionTable.retailer_id == retailer_id,
            )
            .first()
        )

        if record:
            return record.id
