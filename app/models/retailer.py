from dataclasses import dataclass


@dataclass(frozen=True)
class Retailer:
    id: int
    name: str
    owner_id: int
