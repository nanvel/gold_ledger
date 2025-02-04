from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DisplayUser:
    id: int
    email: str
    name: Optional[str]

    @property
    def display_name(self) -> str:
        return self.name or self.email
