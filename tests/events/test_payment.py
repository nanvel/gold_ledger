from decimal import Decimal

from app.events import PaymentEvent
from app.models import (
    ActivityType,
    DisplayPayment,
    DisplayRetailer,
    DisplaySupplier,
    DisplayUser,
    PaymentStatus,
    PaymentType,
)


def test_payment_event():
    payment = DisplayPayment(
        id=1,
        type=PaymentType.CASH.slug,
        date="2021-01-01",
        weight=Decimal(10),
        quality=Decimal(95),
        amount=Decimal(100),
        supplier=DisplaySupplier(id=1, name="Supplier"),
        retailer=DisplayRetailer(id=1, name="Retailer"),
        creator=DisplayUser(id=1, name="User", email="user@mail.com"),
        confirmed_by=DisplayUser(id=2, name="User", email="confirmed@mail.com"),
        rejected_by=DisplayUser(id=3, name="User", email="rejected@mail.com"),
        cancelled_by=DisplayUser(id=4, name="User", email="cancelled@mail.com"),
        created_at=1614556800,
        status=PaymentStatus.CONFIRMED.slug,
    )

    event = PaymentEvent(payment=payment, activity_type=ActivityType.PAYMENT_ADDED)
    assert event.message == "User (1:Retailer) has added a payment of cash 100₹"

    event = PaymentEvent(payment=payment, activity_type=ActivityType.PAYMENT_CANCELLED)
    assert event.message == "User (1:Retailer) has cancelled cash 100₹ payment"

    event = PaymentEvent(payment=payment, activity_type=ActivityType.PAYMENT_CONFIRMED)
    assert event.message == "User (1:Supplier) has confirmed cash 100₹ payment"

    event = PaymentEvent(payment=payment, activity_type=ActivityType.PAYMENT_REJECTED)
    assert event.message == "User (1:Supplier) has rejected cash 100₹ payment"
