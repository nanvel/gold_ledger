from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class CacheTable(Base):
    __tablename__ = "cache"

    id: Mapped[int]
    supplier_id: Mapped[int] = mapped_column(sa.ForeignKey("suppliers.id"))
    retailer_id: Mapped[int] = mapped_column(sa.ForeignKey("retailers.id"), index=True)

    cash_products: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    cash_payments: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    cash_due_date: Mapped[datetime] = mapped_column(nullable=True)
    cash_to_pay: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    rtgs_products: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    rtgs_payments: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    rtgs_due_date: Mapped[datetime] = mapped_column(nullable=True)
    rtgs_to_pay: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    fine_products: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    fine_payments: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    fine_due_date: Mapped[datetime] = mapped_column(nullable=True)
    fine_to_pay: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)

    version: Mapped[int] = mapped_column(server_default="1")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        sa.PrimaryKeyConstraint("id"),
        sa.Index(
            "idx_cache_supplier_retailer",
            "supplier_id",
            "retailer_id",
        ),
    )
