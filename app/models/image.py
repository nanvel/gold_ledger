from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Image:
    id: int
    url: str
    thumb_url: str
    size: int
    width: int
    height: int
    uploaded_by: Optional[int] = None
    supplier_id: Optional[int] = None
    retailer_id: Optional[int] = None
