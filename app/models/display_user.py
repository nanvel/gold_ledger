from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DisplayUser:
    id: int
    email: str
    name: Optional[str]
