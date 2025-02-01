from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ActivityTypeValue:
    value: int
    label: str


class ActivityType(int, Enum):
    PRODUCT_GIVEN = ActivityTypeValue(value=1, label="Product Given")
    PRODUCT_CONFIRMED = ActivityTypeValue(value=2, label="Product Confirmed")
    PRODUCT_REJECTED = ActivityTypeValue(value=3, label="Product Rejected")
    PAYMENT_ADDED = ActivityTypeValue(value=4, label="Payment Added")
    PAYMENT_CONFIRMED = ActivityTypeValue(value=5, label="Payment Confirmed")
    PAYMENT_REJECTED = ActivityTypeValue(value=6, label="Payment Rejected")
    PRODUCT_CANCELLED = ActivityTypeValue(value=7, label="Product Cancelled")
    PAYMENT_CANCELLED = ActivityTypeValue(value=8, label="Payment Cancelled")

    def __new__(cls, arg):
        obj = int.__new__(cls, arg.value)
        obj._value_ = arg.value
        obj.label = arg.label
        return obj
