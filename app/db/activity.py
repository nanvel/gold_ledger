from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class ActivityTable(Base):
    __tablename__ = "activities"

    id: Mapped[int]
    type: Mapped[int]
    message: Mapped[str]
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    supplier_id: Mapped[int] = mapped_column(
        sa.ForeignKey("suppliers.id"),
        nullable=True,
    )
    retailer_id: Mapped[int] = mapped_column(
        sa.ForeignKey("retailers.id"),
        nullable=True,
    )
    product_id: Mapped[int] = mapped_column(sa.ForeignKey("products.id"), nullable=True)
    payment_id: Mapped[int] = mapped_column(sa.ForeignKey("payments.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        sa.PrimaryKeyConstraint("id"),
        sa.Index(
            "idx_activity_supplier_created",
            "supplier_id",
            "created_at",
        ),
        sa.Index(
            "idx_activity_retailer_created",
            "retailer_id",
            "created_at",
        ),
    )
