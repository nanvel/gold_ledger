from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import ActivityTable
from app.models import Activity, ActivityType, DisplayActivity, Timestamp


class ActivitiesRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, activity: Activity) -> int:
        record = ActivityTable(
            type=activity.type.value,
            user_id=activity.user_id,
            supplier_id=activity.supplier_id,
            retailer_id=activity.retailer_id,
            product_id=activity.product_id,
            payment_id=activity.payment_id,
            message=activity.message,
        )

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return record.id

    def filter(
        self,
        supplier_id: Optional[int] = None,
        retailer_id: Optional[int] = None,
        product_id: Optional[int] = None,
        payment_id: Optional[int] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[int, Tuple[DisplayActivity, ...]]:
        query = self._session.query(ActivityTable)

        if supplier_id:
            query = query.filter(ActivityTable.supplier_id == supplier_id)

        if retailer_id:
            query = query.filter(ActivityTable.retailer_id == retailer_id)

        if product_id:
            query = query.filter(ActivityTable.product_id == product_id)

        if payment_id:
            query = query.filter(ActivityTable.payment_id == payment_id)

        total = query.count()
        items = (
            query.order_by(ActivityTable.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        return total, tuple(
            DisplayActivity(
                id=item.id,
                type=ActivityType(item.type).label,
                product_id=item.product_id,
                payment_id=item.payment_id,
                message=item.message,
                created_at=int(Timestamp.from_datetime(item.created_at)),
            )
            for item in items
        )
