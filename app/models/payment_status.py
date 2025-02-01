from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class PaymentStatusValue:
    value: int
    label: str
    slug: str


class PaymentStatus(int, Enum):
    PENDING = PaymentStatusValue(value=1, label="Pending", slug="pending")
    CONFIRMED = PaymentStatusValue(value=2, label="Confirmed", slug="confirmed")
    REJECTED = PaymentStatusValue(value=3, label="Rejected", slug="rejected")
    CANCELED = PaymentStatusValue(value=4, label="Canceled", slug="canceled")

    def __new__(cls, arg):
        obj = int.__new__(cls, arg.value)
        obj._value_ = arg.value
        obj.label = arg.label
        obj.slug = arg.slug
        return obj
