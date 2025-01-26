from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from .payment_type import PaymentType


@dataclass(frozen=True)
class Payment:
    id: int
    type: PaymentType
    date: date
    weight: Decimal
    quality: Decimal
    rate_per_gram: Decimal
    total_amount: Decimal
    supplier_id: int
    retailer_id: int
    creator_id: int
