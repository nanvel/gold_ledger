from dataclasses import dataclass

from app.models import ActivityType, DisplayPayment
from .base import Event


@dataclass(frozen=True)
class PaymentEvent(Event):
    payment: DisplayPayment
    activity_type: ActivityType
