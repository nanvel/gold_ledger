from dataclasses import dataclass

from .base import Event


@dataclass(frozen=True)
class ProductUpdated(Event):
    product_id: int
    supplier_id: int
    retailer_id: int
    message: str
