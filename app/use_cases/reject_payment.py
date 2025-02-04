from fastapi import HTTPException, status

from app.message_bus import MessageBus
from app.models import User
from app.repos.uow import UnitOfWork


class RejectPayment:
    def __init__(self, uow: UnitOfWork, message_bus: MessageBus):
        self._uow = uow
        self._message_bus = message_bus

    def __call__(self, user: User, payment_id: int):
        with self._uow:
            payment = self._uow.payments.by_id(payment_id)

            if not payment or payment.supplier_id != user.supplier_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The product was not found",
                )

            payment = payment.reject(user)
            self._uow.payments.update(payment)
