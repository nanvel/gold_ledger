from dataclasses import dataclass

from app.models import ActivityType, DisplayProduct
from .base import Event


@dataclass(frozen=True)
class ProductEvent(Event):
    product: DisplayProduct
    activity_type: ActivityType
    user_id: int

    @property
    def message(self) -> str:
        if self.activity_type == ActivityType.PRODUCT_ADDED:
            return (
                f"{self.product.creator.display_name} ({self.product.supplier.display_name}) "
                f"has added a product {self.product.display_name}"
            )
        elif self.activity_type == ActivityType.PRODUCT_CONFIRMED:
            return (
                f"{self.product.confirmed_by.display_name} ({self.product.retailer.display_name}) "
                f"has confirmed {self.product.display_name}"
            )
        elif self.activity_type == ActivityType.PRODUCT_REJECTED:
            return (
                f"{self.product.rejected_by.display_name} ({self.product.retailer.display_name}) "
                f"has rejected {self.product.display_name}"
            )
        elif self.activity_type == ActivityType.PRODUCT_CANCELLED:
            return (
                f"{self.product.cancelled_by.display_name} ({self.product.supplier.display_name}) "
                f"has cancelled {self.product.display_name}"
            )
        else:
            raise ValueError(f"Unknown product activity type: {self.activity_type}")
