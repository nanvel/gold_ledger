from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from .display_retailer import DisplayRetailer
from .display_supplier import DisplaySupplier
from .display_user import DisplayUser
from .payment_type import PaymentType
from .timestamp import Timestamp


@dataclass(frozen=True)
class DisplayPayment:
    id: int
    type: str
    date: str
    weight: Optional[Decimal]
    quality: Optional[Decimal]
    amount: Optional[Decimal]
    note: Optional[str]
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

    def to_dict(self) -> dict:
        return {
            "ID": self.id,
            "Type": self.type,
            "Date": self.date,
            "Status": self.status,
            "Supplier": f"{self.supplier.id}:{self.supplier.name}",
            "Retailer": f"{self.retailer.id}:{self.retailer.name}",
            "Amount": str(self.amount or ""),
            "Weight": str(self.weight or ""),
            "Quality": str(self.quality or ""),
            "Note": self.note or "",
            "Created by": f"{self.creator.email}:{self.creator.name}",
            "Created at": Timestamp(self.created_at).to_datetime().isoformat(),
            "Confirmed by": (
                f"{self.confirmed_by.email}:{self.confirmed_by.name}"
                if self.confirmed_by
                else ""
            ),
            "Rejected by": (
                f"{self.rejected_by.email}:{self.rejected_by.name}"
                if self.rejected_by
                else ""
            ),
            "Cancelled by": (
                f"{self.cancelled_by.email}:{self.cancelled_by.name}"
                if self.cancelled_by
                else ""
            ),
        }
