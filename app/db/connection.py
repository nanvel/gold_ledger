from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class ConnectionTable(Base):
    __tablename__ = "connections"

    id: Mapped[int]
    supplier_id: Mapped[int] = mapped_column(sa.ForeignKey("suppliers.id"), index=True)
    retailer_id: Mapped[int] = mapped_column(sa.ForeignKey("retailers.id"), index=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (sa.PrimaryKeyConstraint("id"),)
