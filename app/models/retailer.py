from dataclasses import dataclass


@dataclass(frozen=True)
class Retailer:
    id: int
    name: str
    admin_id: int
