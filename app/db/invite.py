from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class InviteTable(Base):
    __tablename__ = "invites"

    id: Mapped[int]
    supplier_id: Mapped[Optional[int]] = mapped_column(
        sa.ForeignKey("suppliers.id"), nullable=True
    )
    retailer_id: Mapped[Optional[int]] = mapped_column(
        sa.ForeignKey("retailers.id"), nullable=True
    )
    code: Mapped[str] = mapped_column(sa.String(20), index=True, unique=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
    applied_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    __table_args__ = (sa.PrimaryKeyConstraint("id"),)
