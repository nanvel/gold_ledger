from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class UserRoleValue:
    value: int
    label: str
    slug: str


class UserRole(int, Enum):
    ADMIN = UserRoleValue(value=99, label="Administrator", slug="admin")
    SHOP_OWNER = UserRoleValue(value=2, label="Shop Owner", slug="shop_admin")
    EMPLOYEE = UserRoleValue(value=1, label="Employee", slug="employee")

    def __new__(cls, arg):
        obj = int.__new__(cls, arg.value)
        obj._value_ = arg.value
        obj.label = arg.label
        obj.slug = arg.slug
        return obj
