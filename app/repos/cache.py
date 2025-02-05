from sqlalchemy.orm import Session

from app.db import ActivityTable
from app.models import Activity, ActivityType, DisplayActivity, Timestamp


class CacheRepo:
    def __init__(self, session: Session):
        self._session = session

    def create_or_update(self, activity: Activity) -> int:
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
