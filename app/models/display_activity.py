from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DisplayActivity:
    id: int
    type: str
    product_id: Optional[int]
    payment_id: Optional[int]
    message: str
    created_at: int
