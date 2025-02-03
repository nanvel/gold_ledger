from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from .display_retailer import DisplayRetailer
from .display_supplier import DisplaySupplier
from .display_user import DisplayUser
from .payment_type import PaymentType


@dataclass(frozen=True)
class DisplayPayment:
    id: int
    type: str
    date: str
    weight: Optional[Decimal]
    quality: Optional[Decimal]
    amount: Optional[Decimal]
    supplier: DisplaySupplier
    retailer: DisplayRetailer
    creator: DisplayUser
    confirmed_by: Optional[DisplayUser]
    rejected_by: Optional[DisplayUser]
    cancelled_by: Optional[DisplayUser]
    created_at: int
    status: str

    @property
    def display_amount(self) -> str:
        if self.type == PaymentType.FINE.slug:
            return f"{self.type} {self.weight}g {self.quality}%"
        else:
            return f"{self.type} {self.amount}₹"
