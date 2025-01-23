from dataclasses import dataclass
from decimal import Decimal

from .timestamp import Timestamp


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    date: Timestamp
    weight: Decimal
    quality: Decimal
    rate_per_gram: Decimal
    total_amount: Decimal
    custom_fields: dict
    supplier_id: int
    retailer_id: int
    creator_id: int
