from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from .payment_type import PaymentType


@dataclass(frozen=True)
class Payment:
    id: int
    type: PaymentType
    date: date
    weight: Optional[Decimal]
    quality: Optional[Decimal]
    rate_per_gram: Optional[Decimal]
    total_amount: Decimal
    supplier_id: int
    retailer_id: int
    creator_id: int
    confirmed_by: int
    rejected_by: int

    def validate(self):
        if self.type == PaymentType.GOODS:
            assert self.weight is not None
            assert self.quality is not None
            assert self.rate_per_gram is not None
        else:
            assert self.weight is None
            assert self.quality is None
            assert self.rate_per_gram is None
