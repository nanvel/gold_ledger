from app.models import Activity, ActivityType
from app.repos.uow import UnitOfWork


class ActivityMessageFactory:
    def __init__(self):
        pass

    def from_activity(self, activity: Activity, uow: UnitOfWork) -> str:
        if activity.type == ActivityType.PRODUCT_GIVEN:
            return ""
