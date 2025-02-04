from dataclasses import dataclass

from app.models import ActivityType, DisplayPayment
from .base import Event


@dataclass(frozen=True)
class PaymentEvent(Event):
    payment: DisplayPayment
    activity_type: ActivityType
    user_id: int

    @property
    def message(self) -> str:
        if self.activity_type == ActivityType.PAYMENT_ADDED:
            return (
                f"{self.payment.creator.display_name} ({self.payment.retailer.display_name}) "
                f"has added a payment of {self.payment.display_amount}"
            )
        elif self.activity_type == ActivityType.PAYMENT_CONFIRMED:
            return (
                f"{self.payment.confirmed_by.display_name} ({self.payment.supplier.display_name}) "
                f"has confirmed {self.payment.display_amount} payment"
            )
        elif self.activity_type == ActivityType.PAYMENT_REJECTED:
            return (
                f"{self.payment.rejected_by.display_name} ({self.payment.supplier.display_name}) "
                f"has rejected {self.payment.display_amount} payment"
            )
        elif self.activity_type == ActivityType.PAYMENT_CANCELLED:
            return (
                f"{self.payment.cancelled_by.display_name} ({self.payment.retailer.display_name}) "
                f"has cancelled {self.payment.display_amount} payment"
            )
        else:
            raise ValueError(f"Unknown payment activity type: {self.activity_type}")
