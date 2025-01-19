from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import ProductTable
from app.models import Product, Timestamp


@dataclass(frozen=True)
class ProductSearchItem:
    id: int
    name: str
    date: int
    weight: Decimal
    qualify: Decimal
    rate_per_gram: Decimal
    total_amount: Decimal
    created_at: int


class ProductsRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, product: Product):
        record = ProductTable(
            name=product.name,
            date=product.date.to_datetime(),
            weight=product.weight,
            quality=product.quality,
            rate_per_gram=product.rate_per_gram,
            total_amount=product.total_amount,
            custom_fields=product.custom_fields,
            picture=product.picture,
            supplier_id=product.supplier_id,
            retailer_id=product.retailer_id,
            creator_id=product.creator_id,
        )

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return record.id

    def filter(
        self,
        supplier_id: Optional[int],
        retailer_id: Optional[int],
        limit: int,
        offset: int,
    ) -> Tuple[int, Tuple[ProductSearchItem, ...]]:
        query = self._session.query(ProductTable)

        if supplier_id:
            query = query.filter(ProductTable.supplier_id == supplier_id)
        if retailer_id:
            query = query.filter(ProductTable.retailer_id == retailer_id)

        total = query.count()

        records = query.offset(offset).limit(limit)

        return total, tuple(
            ProductSearchItem(
                id=record.id,
                name=record.name,
                date=int(Timestamp.from_datetime(record.date)),
                weight=record.weight,
                qualify=record.quality,
                rate_per_gram=record.rate_per_gram,
                total_amount=record.total_amount,
                created_at=int(Timestamp.from_datetime(record.created_at)),
            )
            for record in records
        )
