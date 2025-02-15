from dataclasses import dataclass
from secrets import token_urlsafe
from typing import Optional


@dataclass(frozen=True)
class Invite:
    id: int
    supplier_id: Optional[int]
    retailer_id: Optional[int]
    code: str

    @classmethod
    def generate_code(cls) -> str:
        return token_urlsafe(16)[:16]
