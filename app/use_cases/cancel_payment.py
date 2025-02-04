from fastapi import HTTPException, status

from app.events import PaymentEvent
from app.message_bus import MessageBus
from app.models import ActivityType, User
from app.repos.uow import UnitOfWork


class CancelPayment:
    def __init__(self, uow: UnitOfWork, message_bus: MessageBus):
        self._uow = uow
        self._message_bus = message_bus

    def __call__(self, user: User, payment_id: int):
        with self._uow:
            payment = self._uow.payments.by_id(payment_id)

            if not payment or payment.retailer_id != user.retailer_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The product was not found",
                )

            payment = payment.cancel(user)
            self._uow.payments.update(payment)

            payment_display = self._uow.payments.display(payment_id)

            self._message_bus.handle(
                PaymentEvent(
                    activity_type=ActivityType.PAYMENT_CANCELLED,
                    payment=payment_display,
                )
            )
