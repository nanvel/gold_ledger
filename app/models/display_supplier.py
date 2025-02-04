from dataclasses import dataclass


@dataclass(frozen=True)
class DisplaySupplier:
    id: int
    name: str

    @property
    def display_name(self) -> str:
        return f"{self.id}:{self.name}"
