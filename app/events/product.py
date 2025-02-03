from dataclasses import dataclass

from app.models import ActivityType, DisplayProduct
from .base import Event


@dataclass(frozen=True)
class ProductEvent(Event):
    product: DisplayProduct
    activity_type: ActivityType
