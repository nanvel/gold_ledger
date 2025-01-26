from dataclasses import dataclass

from .activity_type import ActivityType


@dataclass(frozen=True)
class Activity:
    type: ActivityType
    user_id: int
    supplier_id: int
    retailer_id: int
    product_id: int
    payment_id: int
    message: str
