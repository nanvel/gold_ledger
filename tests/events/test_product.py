from decimal import Decimal

from app.events import ProductEvent
from app.models import (
    ActivityType,
    DisplayProduct,
    DisplayRetailer,
    DisplaySupplier,
    DisplayUser,
    PaymentType,
    ProductStatus,
)


def test_product_event():
    product = DisplayProduct(
        id=1,
        name="Product",
        date="2021-01-01",
        weight=Decimal(10),
        quality=Decimal(95),
        rate=Decimal(100),
        payment_type=PaymentType.CASH.slug,
        payment_amount=Decimal(100),
        payment_weight=Decimal(10),
        payment_quality=Decimal(95),
        payment_due_date="2021-01-10",
        supplier=DisplaySupplier(id=1, name="Supplier"),
        retailer=DisplayRetailer(id=1, name="Retailer"),
        creator=DisplayUser(id=1, name="User", email="user@mail.com"),
        confirmed_by=DisplayUser(id=2, name="User", email="confirmed@mail.com"),
        rejected_by=DisplayUser(id=3, name="User", email="rejected@mail.com"),
        cancelled_by=DisplayUser(id=4, name="User", email="cancelled@mail.com"),
        created_at=1614556800,
        status=ProductStatus.CONFIRMED.slug,
        images=tuple(),
    )

    event = ProductEvent(
        product=product, activity_type=ActivityType.PRODUCT_ADDED, user_id=1
    )
    assert event.message == "User (1:Supplier) has added a product Product (10g 95%)"

    event = ProductEvent(
        product=product, activity_type=ActivityType.PRODUCT_CANCELLED, user_id=1
    )
    assert event.message == "User (1:Supplier) has cancelled Product (10g 95%)"

    event = ProductEvent(
        product=product, activity_type=ActivityType.PRODUCT_CONFIRMED, user_id=1
    )
    assert event.message == "User (1:Retailer) has confirmed Product (10g 95%)"

    event = ProductEvent(
        product=product, activity_type=ActivityType.PRODUCT_REJECTED, user_id=1
    )
    assert event.message == "User (1:Retailer) has rejected Product (10g 95%)"
