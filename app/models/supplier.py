from dataclasses import dataclass


@dataclass
class Supplier:
    id: int
    name: str
    admin_id: int
