from dataclasses import dataclass
from decimal import Decimal
from typing import List

from .due_payment import DuePayment


@dataclass(frozen=True)
class Cache:
    supplier_id: int
    retailer_id: int
    cash_products: Decimal
    cash_payments: Decimal
    rtgs_products: Decimal
    rtgs_payments: Decimal
    fine_products: Decimal
    fine_payments: Decimal
    due_payments: List[DuePayment]
