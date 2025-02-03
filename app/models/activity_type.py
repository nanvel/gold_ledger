from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ActivityTypeValue:
    value: int
    label: str


class ActivityType(int, Enum):
    PRODUCT_ADDED = ActivityTypeValue(value=1, label="Product Added")
    PRODUCT_CONFIRMED = ActivityTypeValue(value=2, label="Product Confirmed")
    PRODUCT_REJECTED = ActivityTypeValue(value=3, label="Product Rejected")
    PRODUCT_CANCELLED = ActivityTypeValue(value=4, label="Product Cancelled")

    PAYMENT_ADDED = ActivityTypeValue(value=11, label="Payment Added")
    PAYMENT_CONFIRMED = ActivityTypeValue(value=12, label="Payment Confirmed")
    PAYMENT_REJECTED = ActivityTypeValue(value=13, label="Payment Rejected")
    PAYMENT_CANCELLED = ActivityTypeValue(value=14, label="Payment Cancelled")

    def __new__(cls, arg):
        obj = int.__new__(cls, arg.value)
        obj._value_ = arg.value
        obj.label = arg.label
        return obj
