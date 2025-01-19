from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


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
    picture: Mapped[dict] = mapped_column(type_=sa.JSON)
    supplier_id: Mapped[int] = mapped_column(sa.ForeignKey("supplier_stores.id"))
    retailer_id: Mapped[int] = mapped_column(
        sa.ForeignKey("retailer_stores.id"), index=True
    )
    creator_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))

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
