from dataclasses import dataclass


@dataclass(frozen=True)
class DisplayRetailer:
    id: int
    name: str
