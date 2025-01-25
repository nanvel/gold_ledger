from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class SupplierTable(Base):
    __tablename__ = "suppliers"

    id: Mapped[int]
    name: Mapped[str] = mapped_column(unique=True)
    owner_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (sa.PrimaryKeyConstraint("id"),)
