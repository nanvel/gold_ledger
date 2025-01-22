from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base


class ImageTable(Base):
    __tablename__ = "images"

    id: Mapped[int]
    url: Mapped[str]
    thumb_url: Mapped[str]
    size: Mapped[int]
    width: Mapped[int]
    height: Mapped[int]

    uploaded_by: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))
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
