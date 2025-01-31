from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class PaymentTypeValue:
    value: int
    label: str
    slug: str


class PaymentType(int, Enum):
    CASH = PaymentTypeValue(value=1, label="Cash", slug="cash")
    RTGS = PaymentTypeValue(value=2, label="RTGS", slug="rtgs")
    FINE = PaymentTypeValue(value=3, label="Fine", slug="fine")

    def __new__(cls, arg):
        obj = int.__new__(cls, arg.value)
        obj._value_ = arg.value
        obj.label = arg.label
        obj.slug = arg.slug
        return obj
