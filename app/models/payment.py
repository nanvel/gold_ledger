from dataclasses import dataclass


@dataclass(frozen=True)
class Payment:
    id: int
    type: int
    date: int
    amount: int
    supplier_id: int
    retailer_id: int
