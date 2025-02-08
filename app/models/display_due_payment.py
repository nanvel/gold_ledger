from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class DisplayDuePayment:
    type: str
    date: str
    amount: Decimal
