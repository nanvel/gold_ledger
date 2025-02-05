from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class Cache:
    supplier_id: int
    retailer_id: int
    cash_products: Decimal
    cash_payments: Decimal
    cash_due_date: Optional[date]
    cash_to_pay: Decimal
    rtgs_products: Decimal
    rtgs_payments: Decimal
    rtgs_due_date: Optional[date]
    rtgs_to_pay: Decimal
    fine_products: Decimal
    fine_payments: Decimal
    fine_due_date: Optional[date]
    fine_to_pay: Decimal
