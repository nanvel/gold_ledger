import logging

from app.events import Event, PaymentEvent, ProductEvent
from app.models import Activity
from app.repos.uow import UnitOfWork

logger = logging.getLogger(__name__)


class MessageBus:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def handle(self, event: Event):
        try:
            if isinstance(event, PaymentEvent):
                activity = Activity(
                    id=0,
                    type=event.activity_type,
                    user_id=event.user_id,
                    supplier_id=event.payment.supplier.id,
                    retailer_id=event.payment.retailer.id,
                    payment_id=event.payment.id,
                    product_id=None,
                    message=event.message,
                )
                self._uow.activities.create(activity)

            elif isinstance(event, ProductEvent):
                activity = Activity(
                    id=0,
                    type=event.activity_type,
                    user_id=event.user_id,
                    supplier_id=event.product.supplier.id,
                    retailer_id=event.product.retailer.id,
                    payment_id=None,
                    product_id=event.product.id,
                    message=event.message,
                )
                self._uow.activities.create(activity)
        except Exception:
            logger.exception(f"{type(event)} event error.")
