from dataclasses import replace
from datetime import date
from decimal import Decimal

from app.factories.activity_message import ActivityMessageFactory
from app.models import (
    Activity,
    ActivityType,
    Payment,
    PaymentType,
    Product,
    Retailer,
    Supplier,
    User,
)


def test_activity_message_factory(container):
    uow = container.uow()
    with uow:
        user = User(
            id=0,
            username="test@mail.com",
            name="User Name",
            password_hash="password",
            token_version=0,
            supplier_id=None,
            retailer_id=None,
        )
        user_id = uow.users.create(user)
        user = replace(user, id=user_id)
        supplier = Supplier(id=0, name="Supplier Name", owner_id=user_id)
        supplier_id = uow.suppliers.create(supplier)
        supplier = replace(supplier, id=supplier_id)
        retailer = Retailer(id=0, name="Retailer Name", owner_id=user_id)
        retailer_id = uow.retailers.create(retailer)
        retailer = replace(retailer, id=retailer_id)

        product = Product(
            id=0,
            name="Product Name",
            date=date(2021, 1, 1),
            supplier_id=supplier_id,
            retailer_id=retailer_id,
            weight=Decimal(1),
            quality=Decimal(100),
            rate_per_gram=Decimal(100),
            total_amount=Decimal(100),
            payment_type=PaymentType.CASH,
            payment_due_date=date(2021, 1, 10),
            creator_id=user_id,
            confirmed_by=None,
            rejected_by=None,
            custom_fields={},
        )
        product_id = uow.products.create(product)
        product = replace(product, id=product_id)

        payment = Payment(
            id=0,
            type=PaymentType.CASH,
            date=date(2021, 1, 1),
            total_amount=Decimal(100),
            supplier_id=supplier_id,
            retailer_id=retailer_id,
            creator_id=user_id,
            confirmed_by=None,
            rejected_by=None,
            weight=None,
            quality=None,
        )
        payment_id = uow.payments.create(payment)
        payment = replace(payment, id=payment_id)

        factory = ActivityMessageFactory()

        assert (
            factory.from_activity(
                Activity(
                    id=0,
                    type=ActivityType.PRODUCT_GIVEN,
                    user_id=user_id,
                    supplier_id=supplier_id,
                    retailer_id=retailer_id,
                    product_id=product_id,
                    payment_id=None,
                    message="",
                ),
                uow=uow,
            )
            == f"User Name ({supplier_id}:Supplier Name) has given "
            f"Product Name to {retailer_id}:Retailer Name"
        )

        assert (
            factory.from_activity(
                Activity(
                    id=0,
                    type=ActivityType.PRODUCT_CONFIRMED,
                    user_id=user_id,
                    supplier_id=supplier_id,
                    retailer_id=retailer_id,
                    product_id=product_id,
                    payment_id=None,
                    message="",
                ),
                uow=uow,
            )
            == f"User Name ({retailer_id}:Retailer Name) has received Product Name"
        )

        assert (
            factory.from_activity(
                Activity(
                    id=0,
                    type=ActivityType.PRODUCT_REJECTED,
                    user_id=user_id,
                    supplier_id=supplier_id,
                    retailer_id=retailer_id,
                    product_id=product_id,
                    payment_id=None,
                    message="",
                ),
                uow=uow,
            )
            == f"User Name ({retailer_id}:Retailer Name) has rejected Product Name"
        )

        assert (
            factory.from_activity(
                Activity(
                    id=0,
                    type=ActivityType.PAYMENT_ADDED,
                    user_id=user_id,
                    supplier_id=supplier_id,
                    retailer_id=retailer_id,
                    product_id=None,
                    payment_id=payment_id,
                    message="",
                ),
                uow=uow,
            )
            == f"User Name ({retailer_id}:Retailer Name) has added a payment of ₹100 (Cash)"
        )

        assert (
            factory.from_activity(
                Activity(
                    id=0,
                    type=ActivityType.PAYMENT_CONFIRMED,
                    user_id=user_id,
                    supplier_id=supplier_id,
                    retailer_id=retailer_id,
                    product_id=None,
                    payment_id=payment_id,
                    message="",
                ),
                uow=uow,
            )
            == f"User Name ({supplier_id}:Supplier Name) has confirmed a payment of ₹100 (Cash)"
        )

        assert (
            factory.from_activity(
                Activity(
                    id=0,
                    type=ActivityType.PAYMENT_REJECTED,
                    user_id=user_id,
                    supplier_id=supplier_id,
                    retailer_id=retailer_id,
                    product_id=None,
                    payment_id=payment_id,
                    message="",
                ),
                uow=uow,
            )
            == f"User Name ({supplier_id}:Supplier Name) has rejected a payment of ₹100 (Cash)"
        )
