from datetime import datetime
from decimal import Decimal
from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base
from .image import ImageTable


product_image_association = sa.Table(
    "product_images",
    Base.metadata,
    sa.Column("product_id", sa.ForeignKey("products.id"), nullable=False),
    sa.Column("image_id", sa.ForeignKey("images.id"), nullable=False),
    sa.Index("idx_product_images_product_image", "product_id", "image_id", unique=True),
)


class ProductTable(Base):
    __tablename__ = "products"

    id: Mapped[int]
    name: Mapped[str]
    date: Mapped[datetime]
    weight: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    quality: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    rate_per_gram: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    total_amount: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    custom_fields: Mapped[dict] = mapped_column(type_=sa.JSON)
    supplier_id: Mapped[int] = mapped_column(sa.ForeignKey("suppliers.id"))
    retailer_id: Mapped[int] = mapped_column(sa.ForeignKey("retailers.id"), index=True)
    creator_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))

    images: Mapped[List[ImageTable]] = relationship(secondary=product_image_association)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        sa.PrimaryKeyConstraint("id"),
        sa.Index(
            "idx_products_supplier_retailer_created",
            "supplier_id",
            "retailer_id",
            "created_at",
        ),
    )
