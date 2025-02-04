from fastapi import HTTPException, status

from app.events.product import ProductEvent
from app.message_bus import MessageBus
from app.models import ActivityType, User
from app.repos.uow import UnitOfWork


class CancelProduct:
    def __init__(self, uow: UnitOfWork, message_bus: MessageBus):
        self._uow = uow
        self._message_bus = message_bus

    def __call__(self, user: User, product_id: int):
        with self._uow:
            product = self._uow.products.by_id(product_id)

            if not product or product.supplier_id != user.supplier_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The product was not found",
                )

            product = product.cancel(user)
            self._uow.products.update(product)

            product_display = self._uow.products.display(product_id)

            self._message_bus.handle(
                ProductEvent(
                    activity_type=ActivityType.PRODUCT_CANCELLED,
                    product=product_display,
                    user_id=user.id,
                )
            )
