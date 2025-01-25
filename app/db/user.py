from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int]
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    # increase to disable issued access tokens
    token_version: Mapped[int] = mapped_column(default=0, server_default="0")
    name: Mapped[str] = mapped_column(nullable=True)

    supplier_id: Mapped[int] = mapped_column(
        sa.ForeignKey("suppliers.id"), nullable=True
    )
    retailer_id: Mapped[int] = mapped_column(
        sa.ForeignKey("retailers.id"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (sa.PrimaryKeyConstraint("id"),)
