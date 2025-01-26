from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class PaymentTypeValue:
    value: int
    label: str
    slug: str


class PaymentType(int, Enum):
    CASH = PaymentTypeValue(value=1, label="Cash", slug="cash")
    BANK_TRANSFER = PaymentTypeValue(
        value=2, label="Bank Transfer", slug="bank_transfer"
    )
    GOODS = PaymentTypeValue(value=3, label="Goods", slug="goods")

    def __new__(cls, arg):
        obj = int.__new__(cls, arg.value)
        obj._value_ = arg.value
        obj.label = arg.label
        obj.slug = arg.slug
        return obj
