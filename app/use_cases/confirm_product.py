from fastapi import HTTPException, status

from app.message_bus import MessageBus
from app.models import User
from app.repos.uow import UnitOfWork


class ConfirmProduct:
    def __init__(self, uow: UnitOfWork, message_bus: MessageBus):
        self._uow = uow
        self._message_bus = message_bus

    def __call__(self, user: User, product_id: int):
        with self._uow:
            product = self._uow.products.by_id(product_id)

            if not product or product.retailer_id != user.retailer_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The product was not found",
                )

            product = product.confirm(user)
            self._uow.products.update(product)
