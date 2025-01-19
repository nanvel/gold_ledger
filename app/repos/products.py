from sqlalchemy.orm import Session

from app.db import ProductTable
from app.models import Product


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
