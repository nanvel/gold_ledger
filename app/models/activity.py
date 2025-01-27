from dataclasses import dataclass
from typing import Optional

from .activity_type import ActivityType


@dataclass(frozen=True)
class Activity:
    id: int
    type: ActivityType
    user_id: int
    supplier_id: int
    retailer_id: int
    product_id: Optional[int]
    payment_id: Optional[int]
    message: str
