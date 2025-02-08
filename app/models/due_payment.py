from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from .payment_type import PaymentType


@dataclass(frozen=True)
class DuePayment:
    type: PaymentType
    date: date
    amount: Decimal
