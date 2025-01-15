from dataclasses import dataclass


@dataclass
class Product:
    uuid: str
    name: str
    date: str
    weight: float
    quality: str
    rate_per_gram: float
    total_amount: float
    custom_fields: dict
    picture: str
    supplier: int
    retailer: int
