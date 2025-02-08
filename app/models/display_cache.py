from dataclasses import dataclass
from decimal import Decimal
from typing import List

from .display_retailer import DisplayRetailer
from .display_supplier import DisplaySupplier
from .due_payment import DuePayment


@dataclass(frozen=True)
class DisplayCache:
    supplier: DisplaySupplier
    retailer: DisplayRetailer
    cash_products: Decimal
    cash_payments: Decimal
    rtgs_products: Decimal
    rtgs_payments: Decimal
    fine_products: Decimal
    fine_payments: Decimal
    due_payments: List[DuePayment]
