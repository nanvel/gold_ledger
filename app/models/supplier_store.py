from dataclasses import dataclass


@dataclass
class SupplierStore:
    id: int
    name: str
    admin_id: int
