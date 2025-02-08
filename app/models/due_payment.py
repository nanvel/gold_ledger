from dataclasses import dataclass
from decimal import Decimal

from .payment_type import PaymentType


@dataclass(frozen=True)
class DuePayment:
    payment_type: PaymentType
    date: str
    amount: Decimal
