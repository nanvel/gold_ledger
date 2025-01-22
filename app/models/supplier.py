from dataclasses import dataclass


@dataclass(frozen=True)
class Supplier:
    id: int
    name: str
    admin_id: int
