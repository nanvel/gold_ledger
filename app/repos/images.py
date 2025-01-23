from typing import Optional

from sqlalchemy.orm import Session

from app.db import ImageTable
from app.models import Image


class ImagesRepo:
    def __init__(self, session: Session):
        self._session = session

    def create(self, image: Image):
        record = ImageTable(
            url=image.url,
            thumb_url=image.thumb_url,
            size=image.size,
            width=image.width,
            height=image.height,
            uploaded_by=image.uploaded_by,
            supplier_id=image.supplier_id,
            retailer_id=image.retailer_id,
        )

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return record.id

    def by_id(self, image_id: int) -> Optional[Image]:
        record = (
            self._session.query(ImageTable).where(ImageTable.id == image_id).first()
        )
        if record:
            return Image(
                id=record.id,
                url=record.url,
                thumb_url=record.thumb_url,
                size=record.size,
                width=record.width,
                height=record.height,
                uploaded_by=record.uploaded_by,
                supplier_id=record.supplier_id,
                retailer_id=record.retailer_id,
            )
