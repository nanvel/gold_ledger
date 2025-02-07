from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db import ImageTable, ProductTable
from app.models import (
    DisplayProduct,
    DisplayImage,
    DisplayRetailer,
    DisplaySupplier,
    DisplayUser,
    Image,
    PaymentType,
    Product,
    ProductOrderBy,
    ProductStatus,
    Timestamp,
)


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
            status=product.status.value,
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
            record.status = product.status.value

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

    def display(self, product_id: int) -> Optional[DisplayProduct]:
        record = self._session.query(ProductTable).filter_by(id=product_id).first()

        if record:
            return DisplayProduct(
                id=record.id,
                name=record.name,
                date=record.date.isoformat(),
                weight=record.weight,
                quality=record.quality,
                rate=record.rate,
                payment_type=PaymentType(record.payment_type).slug,
                payment_amount=record.payment_amount,
                payment_weight=record.payment_weight,
                payment_quality=record.payment_quality,
                payment_due_date=record.payment_due_date.isoformat(),
                created_at=int(Timestamp.from_datetime(record.created_at)),
                supplier=DisplaySupplier(
                    id=record.supplier.id, name=record.supplier.name
                ),
                retailer=DisplayRetailer(
                    id=record.retailer.id, name=record.retailer.name
                ),
                creator=DisplayUser(
                    id=record.creator.id,
                    name=record.creator.name,
                    email=record.creator.username,
                ),
                images=tuple(
                    DisplayImage(
                        id=image.id,
                        url=image.url,
                        thumb_url=image.thumb_url,
                        size=image.size,
                        width=image.width,
                        height=image.height,
                        created_at=int(Timestamp.from_datetime(image.created_at)),
                    )
                    for image in record.images
                ),
                confirmed_by=(
                    DisplayUser(
                        id=record.confirmed_by_user.id,
                        name=record.confirmed_by_user.name,
                        email=record.confirmed_by_user.username,
                    )
                    if record.confirmed_by
                    else None
                ),
                rejected_by=(
                    DisplayUser(
                        id=record.rejected_by_user.id,
                        name=record.rejected_by_user.name,
                        email=record.rejected_by_user.username,
                    )
                    if record.rejected_by
                    else None
                ),
                cancelled_by=(
                    DisplayUser(
                        id=record.cancelled_by_user.id,
                        name=record.cancelled_by_user.name,
                        email=record.cancelled_by_user.username,
                    )
                    if record.cancelled_by
                    else None
                ),
                status=ProductStatus(record.status).slug,
            )

    def filter(
        self,
        supplier_id: Optional[int],
        retailer_id: Optional[int],
        status: Optional[ProductStatus],
        limit: int,
        offset: int,
        order_by: ProductOrderBy = ProductOrderBy.CREATED,
        reverse: bool = True,
    ) -> Tuple[int, Tuple[DisplayProduct, ...]]:
        query = self._session.query(ProductTable)

        if supplier_id:
            query = query.filter(ProductTable.supplier_id == supplier_id)
        if retailer_id:
            query = query.filter(ProductTable.retailer_id == retailer_id)
        if status:
            query = query.filter(ProductTable.status == status.value)

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
                DisplayProduct(
                    id=record.id,
                    name=record.name,
                    date=record.date.isoformat(),
                    weight=record.weight,
                    quality=record.quality,
                    rate=record.rate,
                    payment_type=PaymentType(record.payment_type).slug,
                    payment_amount=record.payment_amount,
                    payment_weight=record.payment_weight,
                    payment_quality=record.payment_quality,
                    payment_due_date=record.payment_due_date.isoformat(),
                    created_at=int(Timestamp.from_datetime(record.created_at)),
                    images=tuple(
                        DisplayImage(
                            id=image.id,
                            url=image.url,
                            thumb_url=image.thumb_url,
                            size=image.size,
                            width=image.width,
                            height=image.height,
                            created_at=int(Timestamp.from_datetime(image.created_at)),
                        )
                        for image in record.images
                    ),
                    status=ProductStatus(record.status).slug,
                    retailer=DisplayRetailer(
                        id=record.retailer.id, name=record.retailer.name
                    ),
                    supplier=DisplaySupplier(
                        id=record.supplier.id, name=record.supplier.name
                    ),
                    creator=DisplayUser(
                        id=record.creator.id,
                        name=record.creator.name,
                        email=record.creator.username,
                    ),
                    confirmed_by=(
                        DisplayUser(
                            id=record.confirmed_by_user.id,
                            name=record.confirmed_by_user.name,
                            email=record.confirmed_by_user.username,
                        )
                        if record.confirmed_by
                        else None
                    ),
                    rejected_by=(
                        DisplayUser(
                            id=record.rejected_by_user.id,
                            name=record.rejected_by_user.name,
                            email=record.rejected_by_user.username,
                        )
                        if record.rejected_by
                        else None
                    ),
                    cancelled_by=(
                        DisplayUser(
                            id=record.cancelled_by_user.id,
                            name=record.cancelled_by_user.name,
                            email=record.cancelled_by_user.username,
                        )
                        if record.cancelled_by
                        else None
                    ),
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
