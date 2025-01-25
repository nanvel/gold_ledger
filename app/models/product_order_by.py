from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class OrderByValue:
    value: str
    name: str


class ProductOrderBy(str, Enum):
    CREATED = OrderByValue(value="created", name="Created")
    ID = OrderByValue(value="id", name="ID")

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._value_ = args[0].value
        return obj
