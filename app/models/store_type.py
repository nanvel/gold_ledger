from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class StoreTypeValue:
    value: str
    label: str


class StoreType(str, Enum):
    SUPPLIER = StoreTypeValue(value="supplier", label="Supplier")
    RETAILER = StoreTypeValue(value="retailer", label="Retailer")

    def __new__(cls, arg):
        obj = str.__new__(cls, arg.value)
        obj._value_ = arg.value
        obj.label = arg.label
        return obj
