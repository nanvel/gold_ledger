from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.db import ImageTable, ProductTable
from app.models import Image, PaymentType, Product, ProductOrderBy, Timestamp


@dataclass(frozen=True)
class ProductImage:
    id: int
    url: str
    thumb_url: str
    created_at: int


@dataclass(frozen=True)
class ProductStore:
    id: int
    name: str


@dataclass(frozen=True)
class ProductUser:
    id: int
    name: str
    email: str


@dataclass(frozen=True)
class ProductSearchItem:
    id: int
    name: str
    date: str
    weight: Decimal
    quality: Decimal
    rate: Decimal
    payment_type: str
    payment_amount: Optional[Decimal]
    payment_weight: Optional[Decimal]
    payment_quality: Optional[Decimal]
    payment_due_date: str
    created_at: int
    images: Tuple[ProductImage, ...]
    confirmed_by: Optional[int]
    rejected_by: Optional[int]
    cancelled_by: Optional[int]


@dataclass(frozen=True)
class ProductDetailsItem:
    id: int
    name: str
    date: str
    weight: Decimal
    quality: Decimal
    rate: Decimal
    payment_type: str
    payment_amount: Optional[Decimal]
    payment_weight: Optional[Decimal]
    payment_quality: Optional[Decimal]
    payment_due_date: str
    created_at: int
    supplier: ProductStore
    retailer: ProductStore
    creator: ProductUser
    images: Tuple[ProductImage, ...]
    confirmed_by: Optional[ProductUser]
    rejected_by: Optional[ProductUser]
    cancelled_by: Optional[ProductUser]


@dataclass(frozen=True)
class ProductStats:
    total_received: Decimal
    number_received: int
    total_ontime: Decimal


class ProductsRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, product: Product):
        record = ProductTable(
            name=product.name,
            date=product.date,
            weight=product.weight,
            quality=product.quality,
            rate=product.rate,
            payment_type=product.payment_type.value,
            payment_amount=product.payment_amount,
            payment_weight=product.payment_weight,
            payment_quality=product.payment_quality,
            payment_due_date=product.payment_due_date,
            supplier_id=product.supplier_id,
            retailer_id=product.retailer_id,
            creator_id=product.creator_id,
        )

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return record.id

    def update(self, product: Product):
        record = self._session.query(ProductTable).filter_by(id=product.id).first()

        if record:
            record.confirmed_by = product.confirmed_by
            record.rejected_by = product.rejected_by
            record.cancelled_by = product.cancelled_by

            self._session.commit()

    def by_id(self, product_id: int) -> Optional[Product]:
        record = self._session.query(ProductTable).filter_by(id=product_id).first()

        if record:
            return Product(
                id=record.id,
                name=record.name,
                date=record.date,
                weight=record.weight,
                quality=record.quality,
                rate=record.rate,
                payment_type=PaymentType(record.payment_type),
                payment_amount=record.payment_amount,
                payment_weight=record.payment_weight,
                payment_quality=record.payment_quality,
                payment_due_date=record.payment_due_date,
                supplier_id=record.supplier_id,
                retailer_id=record.retailer_id,
                creator_id=record.creator_id,
                confirmed_by=record.confirmed_by,
                rejected_by=record.rejected_by,
                cancelled_by=record.cancelled_by,
            )

    def details(self, product_id: int) -> Optional[ProductDetailsItem]:
        record = self._session.query(ProductTable).filter_by(id=product_id).first()

        if record:
            return ProductDetailsItem(
                id=record.id,
                name=record.name,
                date=record.date.isoformat(),
                weight=record.weight,
                quality=record.quality,
                rate=record.rate,
                payment_type=PaymentType(record.payment_type).label,
                payment_amount=record.payment_amount,
                payment_weight=record.payment_weight,
                payment_quality=record.payment_quality,
                payment_due_date=record.payment_due_date.isoformat(),
                created_at=int(Timestamp.from_datetime(record.created_at)),
                supplier=ProductStore(id=record.supplier.id, name=record.supplier.name),
                retailer=ProductStore(id=record.retailer.id, name=record.retailer.name),
                creator=ProductUser(
                    id=record.creator.id,
                    name=record.creator.name,
                    email=record.creator.username,
                ),
                images=tuple(
                    ProductImage(
                        id=image.id,
                        url=image.url,
                        thumb_url=image.thumb_url,
                        created_at=int(Timestamp.from_datetime(image.created_at)),
                    )
                    for image in record.images
                ),
                confirmed_by=(
                    ProductUser(
                        id=record.confirmed_by_user.id,
                        name=record.confirmed_by_user.name,
                        email=record.confirmed_by_user.username,
                    )
                    if record.confirmed_by
                    else None
                ),
                rejected_by=(
                    ProductUser(
                        id=record.rejected_by_user.id,
                        name=record.rejected_by_user.name,
                        email=record.rejected_by_user.username,
                    )
                    if record.rejected_by
                    else None
                ),
                cancelled_by=(
                    ProductUser(
                        id=record.cancelled_by_user.id,
                        name=record.cancelled_by_user.name,
                        email=record.cancelled_by_user.username,
                    )
                    if record.cancelled_by
                    else None
                ),
            )

    def filter(
        self,
        supplier_id: Optional[int],
        retailer_id: Optional[int],
        limit: int,
        offset: int,
        order_by: ProductOrderBy = ProductOrderBy.CREATED,
        reverse: bool = True,
    ) -> Tuple[int, Tuple[ProductSearchItem, ...]]:
        query = self._session.query(ProductTable)

        if supplier_id:
            query = query.filter(ProductTable.supplier_id == supplier_id)
        if retailer_id:
            query = query.filter(ProductTable.retailer_id == retailer_id)

        total = query.count()

        order_by_field = (
            ProductTable.created_at
            if order_by == ProductOrderBy.CREATED
            else ProductTable.id
        )

        if reverse:
            order_by_field = order_by_field.desc()

        records = query.order_by(order_by_field).offset(offset).limit(limit)

        return (
            total,
            tuple(
                ProductSearchItem(
                    id=record.id,
                    name=record.name,
                    date=record.date.isoformat(),
                    weight=record.weight,
                    quality=record.quality,
                    rate=record.rate,
                    payment_type=PaymentType(record.payment_type).label,
                    payment_amount=record.payment_amount,
                    payment_weight=record.payment_weight,
                    payment_quality=record.payment_quality,
                    payment_due_date=record.payment_due_date.isoformat(),
                    created_at=int(Timestamp.from_datetime(record.created_at)),
                    images=tuple(
                        ProductImage(
                            id=image.id,
                            url=image.url,
                            thumb_url=image.thumb_url,
                            created_at=int(Timestamp.from_datetime(image.created_at)),
                        )
                        for image in record.images
                    ),
                    confirmed_by=record.confirmed_by,
                    rejected_by=record.rejected_by,
                    cancelled_by=record.cancelled_by,
                )
                for record in records
            ),
        )

    def add_image(self, product: Product, image: Image):
        product = (
            self._session.query(ProductTable)
            .where(ProductTable.id == product.id)
            .first()
        )
        image = self._session.query(ImageTable).where(ImageTable.id == image.id).first()

        if product:
            product.images.append(image)

        self._session.commit()

    def stats(
        self,
        supplier_id: Optional[int],
        retailer_id: Optional[int],
    ) -> ProductStats:
        query = self._session.query(
            func.sum(ProductTable.payment_amount).label("total"),
            func.count(ProductTable.id).label("count"),
        )

        if supplier_id:
            query = query.filter(ProductTable.supplier_id == supplier_id)
        if retailer_id:
            query = query.filter(ProductTable.retailer_id == retailer_id)

        total_received, number_received = query.filter(
            ProductTable.confirmed_by.isnot(None)
        ).first() or (Decimal(0), 0)

        total_ontime = query.filter(
            ProductTable.confirmed_by.isnot(None),
            ProductTable.payment_due_date <= func.now(),
        ).scalar() or Decimal(0)

        return ProductStats(
            total_received=total_received or Decimal(0),
            number_received=number_received or 0,
            total_ontime=total_ontime or Decimal(0),
        )
