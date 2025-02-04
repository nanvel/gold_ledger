from dataclasses import replace
from datetime import date
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status

from app.message_bus import MessageBus
from app.models import PaymentType, Product
from app.repos.uow import UnitOfWork


class AddProduct:
    def __init__(self, uow: UnitOfWork, message_bus: MessageBus):
        self._uow = uow
        self._message_bus = message_bus

    def __call__(
        self,
        retailer_id: int,
        supplier_id: int,
        creator_id: int,
        image_id: Optional[int],
        name: str,
        date_: date,
        weight: Decimal,
        quality: Decimal,
        rate: Decimal,
        payment_type: PaymentType,
        payment_amount: Optional[Decimal],
        payment_weight: Optional[Decimal],
        payment_quality: Optional[Decimal],
        payment_due_date: date,
    ):
        with self._uow:
            retailer = self._uow.retailers.by_id(retailer_id)

            if retailer is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The retailer store was not found",
                )

            if image_id:
                image = self._uow.images.by_id(image_id)

                if image is None or not image.supplier_id:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="The image was not found",
                    )

                if image.supplier_id != supplier_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="The image does not belong to the store",
                    )
            else:
                image = None

            product = Product(
                id=0,
                name=name,
                date=date_,
                weight=weight,
                quality=quality,
                rate=rate,
                payment_type=payment_type,
                payment_amount=payment_amount,
                payment_weight=payment_weight,
                payment_quality=payment_quality,
                payment_due_date=payment_due_date,
                supplier_id=supplier_id,
                retailer_id=retailer_id,
                creator_id=creator_id,
                confirmed_by=None,
                rejected_by=None,
                cancelled_by=None,
            )
            product.validate()
            product_id = self._uow.products.create(product)
            product = replace(product, id=product_id)

            if image:
                self._uow.products.add_image(product, image)
