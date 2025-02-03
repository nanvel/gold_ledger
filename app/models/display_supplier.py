from dataclasses import dataclass


@dataclass(frozen=True)
class DisplaySupplier:
    id: int
    name: str
