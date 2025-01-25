from dataclasses import dataclass


@dataclass(frozen=True)
class Supplier:
    id: int
    name: str
    owner_id: int
