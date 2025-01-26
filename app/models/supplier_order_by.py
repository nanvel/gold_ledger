from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class OrderByValue:
    value: str
    name: str


class SupplierOrderBy(str, Enum):
    CREATED = OrderByValue(value="created", name="Created")
    NANE = OrderByValue(value="name", name="Name")

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._value_ = args[0].value
        return obj
