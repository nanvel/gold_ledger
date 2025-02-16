from datetime import datetime

from sqlalchemy.orm import Session

from app.db import InviteTable
from app.models import Invite


class InvitesRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, supplier_id=None, retailer_id=None) -> Invite:
        filters = [InviteTable.applied_at.is_(None)]
        if supplier_id:
            filters.append(InviteTable.supplier_id == supplier_id)
        elif retailer_id:
            filters.append(InviteTable.retailer_id == retailer_id)
        else:
            raise ValueError("Invite must have supplier_id or retailer_id")

        record = self._session.query(InviteTable).filter(*filters).first()

        if not record:
            record = InviteTable(
                supplier_id=supplier_id,
                retailer_id=retailer_id,
                code=Invite.generate_code(),
            )
            self._session.add(record)
            self._session.commit()
            self._session.refresh(record)

        return Invite(
            id=record.id,
            supplier_id=record.supplier_id,
            retailer_id=record.retailer_id,
            code=record.code,
        )

    def get(self, code: str) -> Invite:
        record = (
            self._session.query(InviteTable)
            .filter(
                InviteTable.code == code,
                InviteTable.applied_at.is_(None),
            )
            .first()
        )

        if record:
            return Invite(
                id=record.id,
                supplier_id=record.supplier_id,
                retailer_id=record.retailer_id,
                code=record.code,
            )

    def apply(self, code: str):
        record = (
            self._session.query(InviteTable)
            .filter(
                InviteTable.code == code,
                InviteTable.applied_at.is_(None),
            )
            .first()
        )

        if record:
            record.applied_at = datetime.now()
            self._session.commit()
