from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class PaymentTypeValue:
    value: int
    label: str


class PaymentType(int, Enum):
    CASH = PaymentTypeValue(value=1, label="Cash")
    GOODS = PaymentTypeValue(value=2, label="Goods")

    def __new__(cls, arg):
        obj = int.__new__(cls, arg.value)
        obj._value_ = arg.value
        obj.label = arg.label
        return obj
