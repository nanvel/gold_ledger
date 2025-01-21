from dataclasses import dataclass
from typing import Optional

from .user_role import UserRole


@dataclass(frozen=True)
class User:
    id: int
    username: str
    password_hash: str
    role: UserRole
    token_version: int
    supplier_id: Optional[int]
    retailer_id: Optional[int]

    @property
    def is_supplier(self):
        return self.supplier_id is not None
