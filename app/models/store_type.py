from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class StoreTypeValue:
    value: str
    name: str


class StoreType(str, Enum):
    SUPPLIER = StoreTypeValue(value="supplier", name="Supplier")
    RETAILER = StoreTypeValue(value="retailer", name="Retailer")

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._value_ = args[0].value
        return obj
