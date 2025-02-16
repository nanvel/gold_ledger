from dataclasses import dataclass
from decimal import Decimal
from collections import OrderedDict
from typing import Optional, Tuple

from .display_image import DisplayImage
from .display_retailer import DisplayRetailer
from .display_supplier import DisplaySupplier
from .display_user import DisplayUser
from .timestamp import Timestamp


class FakeFile:
    def __init__(self):
        self.row = ""

    def write(self, data: str):
        self.row = data


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

    def to_dict(self):
        return OrderedDict(
            (
                ("ID", self.id),
                ("Name", self.name),
                ("Date", self.date),
                ("Status", self.status),
                ("Supplier", f"{self.supplier.id}:{self.supplier.name}"),
                ("Retailer", f"{self.retailer.id}:{self.retailer.name}"),
                ("Weight", str(self.weight or "")),
                ("Quality", str(self.quality or "")),
                ("Rate", str(self.rate or "")),
                ("Payment type", self.payment_type),
                ("Payment amount", str(self.payment_amount or "")),
                ("Payment weight", str(self.payment_weight or "")),
                ("Payment quality", str(self.payment_quality or "")),
                ("Payment due_date", str(self.payment_due_date or "")),
                ("Created at", Timestamp(self.created_at).to_datetime().isoformat()),
                ("Created by", f"{self.creator.email}:{self.creator.name}"),
                ("Images", "|".join([image.url for image in self.images])),
                (
                    "Confirmed by",
                    (
                        f"{self.confirmed_by.email}:{self.confirmed_by.name}"
                        if self.confirmed_by
                        else ""
                    ),
                ),
                (
                    "Rejected by",
                    (
                        f"{self.rejected_by.email}:{self.rejected_by.email}"
                        if self.rejected_by
                        else ""
                    ),
                ),
                (
                    "Cancelled by",
                    (
                        f"{self.cancelled_by.email}:{self.cancelled_by.name}"
                        if self.cancelled_by
                        else ""
                    ),
                ),
            )
        )
