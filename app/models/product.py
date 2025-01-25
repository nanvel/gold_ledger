from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    date: date
    weight: Decimal
    quality: Decimal
    rate_per_gram: Decimal
    total_amount: Decimal
    payment_due_date: date
    custom_fields: dict
    supplier_id: int
    retailer_id: int
    creator_id: int
