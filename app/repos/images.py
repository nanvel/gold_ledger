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
