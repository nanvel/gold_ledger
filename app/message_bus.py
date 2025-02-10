import logging

from app.events import Event, PaymentEvent, ProductEvent
from app.models import Activity, ActivityType
from app.repos.uow import UnitOfWork
from app.services.accounting import AccountingService

logger = logging.getLogger(__name__)


class MessageBus:
    def __init__(self, uow: UnitOfWork, accounting_service: AccountingService):
        self._uow = uow
        self._accounting_service = accounting_service

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
                with self._uow:
                    self._uow.activities.create(activity)
                    if event.activity_type == ActivityType.PAYMENT_CONFIRMED:
                        cache = self._accounting_service.compute(
                            supplier_id=event.payment.supplier.id,
                            retailer_id=event.payment.retailer.id,
                        )
                        self._uow.cache.create_or_update(cache)

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
                with self._uow:
                    self._uow.activities.create(activity)
                    if event.activity_type == ActivityType.PRODUCT_CONFIRMED:
                        cache = self._accounting_service.compute(
                            supplier_id=event.product.supplier.id,
                            retailer_id=event.product.retailer.id,
                        )
                        self._uow.cache.create_or_update(cache)

        except Exception:
            logger.exception(f"{type(event)} event error.")
