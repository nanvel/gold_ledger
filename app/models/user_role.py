from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class UserRoleValue:
    value: int
    name: str
    slug: str


class UserRole(int, Enum):
    ADMIN = UserRoleValue(value=99, name="Administrator", slug="admin")
    SHOP_OWNER = UserRoleValue(value=2, name="Shop Owner", slug="shop_admin")
    EMPLOYEE = UserRoleValue(value=1, name="Employee", slug="employee")

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._value_ = args[0].value
        return obj
