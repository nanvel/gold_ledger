from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from .display_image import DisplayImage
from .display_retailer import DisplayRetailer
from .display_supplier import DisplaySupplier
from .display_user import DisplayUser


@dataclass(frozen=True)
class DisplayProduct:
    id: int
    name: str
    date: str
    weight: Decimal
    quality: Decimal
    rate: Decimal
    payment_type: str
    payment_amount: Optional[Decimal]
    payment_weight: Optional[Decimal]
    payment_quality: Optional[Decimal]
    payment_due_date: str
    created_at: int
    supplier: DisplaySupplier
    retailer: DisplayRetailer
    creator: DisplayUser
    images: Tuple[DisplayImage, ...]
    confirmed_by: Optional[DisplayUser]
    rejected_by: Optional[DisplayUser]
    cancelled_by: Optional[DisplayUser]
    status: str

    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.weight}g {self.quality}%)"
