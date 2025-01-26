from datetime import date, datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class PaymentTable(Base):
    __tablename__ = "payments"

    id: Mapped[int]
    date: Mapped[date]
    type: Mapped[int]
    weight: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    quality: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    rate_per_gram: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    total_amount: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL)
    supplier_id: Mapped[int] = mapped_column(sa.ForeignKey("suppliers.id"))
    retailer_id: Mapped[int] = mapped_column(sa.ForeignKey("retailers.id"), index=True)
    creator_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        sa.PrimaryKeyConstraint("id"),
        sa.Index(
            "idx_payments_supplier_retailer_created",
            "supplier_id",
            "retailer_id",
            "created_at",
        ),
    )
