from datetime import date, datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class PaymentTable(Base):
    __tablename__ = "payments"

    id: Mapped[int]
    date: Mapped[date]
    type: Mapped[int]
    weight: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL, nullable=True)
    quality: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL, nullable=True)
    amount: Mapped[Decimal] = mapped_column(type_=sa.DECIMAL, nullable=True)
    supplier_id: Mapped[int] = mapped_column(sa.ForeignKey("suppliers.id"))
    retailer_id: Mapped[int] = mapped_column(sa.ForeignKey("retailers.id"), index=True)
    creator_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
    confirmed_by = mapped_column(sa.ForeignKey("users.id"), nullable=True)
    rejected_by = mapped_column(sa.ForeignKey("users.id"), nullable=True)
    cancelled_by = mapped_column(sa.ForeignKey("users.id"), nullable=True)
    status: Mapped[int] = mapped_column(server_default="1")

    supplier: Mapped["SupplierTable"] = relationship(
        "SupplierTable", foreign_keys=[supplier_id], lazy="joined"
    )
    retailer: Mapped["RetailerTable"] = relationship(
        "RetailerTable", foreign_keys=[retailer_id], lazy="joined"
    )
    creator: Mapped["UserTable"] = relationship(
        "UserTable", foreign_keys=[creator_id], lazy="joined"
    )
    confirmed_by_user: Mapped["UserTable"] = relationship(
        "UserTable", foreign_keys=[confirmed_by], lazy="joined"
    )
    rejected_by_user: Mapped["UserTable"] = relationship(
        "UserTable", foreign_keys=[rejected_by], lazy="joined"
    )
    cancelled_by_user: Mapped["UserTable"] = relationship(
        "UserTable", foreign_keys=[cancelled_by], lazy="joined"
    )

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
