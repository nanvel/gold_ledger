from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class UserRoleValue:
    value: int
    name: str


class UserRole(int, Enum):
    ADMIN = UserRoleValue(value=99, name="Administrator")
    SHOP_OWNER = UserRoleValue(value=2, name="Shop Owner")
    EMPLOYEE = UserRoleValue(value=1, name="Employee")

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._value_ = args[0].value
        return obj
