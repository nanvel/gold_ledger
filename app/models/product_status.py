from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class ProductStatusValue:
    value: int
    label: str
    slug: str


class ProductStatus(int, Enum):
    PENDING = ProductStatusValue(value=1, label="Pending", slug="pending")
    CONFIRMED = ProductStatusValue(value=2, label="Confirmed", slug="confirmed")
    REJECTED = ProductStatusValue(value=3, label="Rejected", slug="rejected")
    CANCELED = ProductStatusValue(value=4, label="Canceled", slug="canceled")

    def __new__(cls, arg):
        obj = int.__new__(cls, arg.value)
        obj._value_ = arg.value
        obj.label = arg.label
        obj.slug = arg.slug
        return obj
