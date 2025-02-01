from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from .payment_type import PaymentType


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    date: date
    weight: Decimal
    quality: Decimal
    rate_per_gram: Decimal
    payment_type: PaymentType
    payment_amount: Optional[Decimal]
    payment_weight: Optional[Decimal]
    payment_quality: Optional[Decimal]
    payment_due_date: date
    supplier_id: int
    retailer_id: int
    creator_id: int
    confirmed_by: Optional[int]
    rejected_by: Optional[int]

    def validate(self):
        if self.payment_type == PaymentType.CASH:
            if self.payment_amount is None:
                raise ValueError("payment_amount is required for CASH payment type")
            if self.payment_weight is not None:
                raise ValueError("payment_weight is not required for CASH payment type")
            if self.payment_quality is not None:
                raise ValueError(
                    "payment_quality is not required for CASH payment type"
                )
        else:
            if self.payment_amount is not None:
                raise ValueError(
                    "payment_amount is not required for WEIGHT payment type"
                )
            if self.payment_weight is None:
                raise ValueError("payment_weight is required for WEIGHT payment type")
            if self.payment_quality is None:
                raise ValueError("payment_quality is required for WEIGHT payment type")
