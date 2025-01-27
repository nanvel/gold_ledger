from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    id: int
    username: str
    password_hash: str
    token_version: int
    supplier_id: Optional[int]
    retailer_id: Optional[int]
    name: Optional[str] = None

    @property
    def is_supplier(self):
        return self.supplier_id is not None

    @property
    def is_retailer(self):
        return self.retailer_id is not None

    @property
    def display_name(self):
        return self.name or self.username
