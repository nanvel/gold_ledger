from dataclasses import replace
from datetime import date
from decimal import Decimal

from app.models import PaymentType, Product, Retailer, Supplier, User


def test_products(container):
    uow = container.uow()
    with uow:
        user = User(
            id=0,
            name="User",
            username="user@example.com",
            password_hash="password",
            token_version=0,
            retailer_id=None,
            supplier_id=None,
        )
        user_id = uow.users.create(user)
        supplier = Supplier(id=0, name="Supplier", owner_id=user_id)
        supplier_id = uow.suppliers.create(supplier)
        retailer = Retailer(id=0, name="Retailer", owner_id=user_id)
        retailer_id = uow.retailers.create(retailer)

        product1 = Product(
            id=0,
            name="Product 1",
            date=date(2021, 1, 1),
            weight=Decimal(1),
            quality=Decimal(1),
            rate_per_gram=Decimal(1),
            total_amount=Decimal(1),
            payment_type=PaymentType.CASH,
            payment_due_date=date(2021, 1, 1),
            supplier_id=supplier_id,
            retailer_id=retailer_id,
            creator_id=user_id,
            confirmed_by=None,
            rejected_by=None,
            custom_fields={},
        )
        product1_id = uow.products.create(product1)
        product2 = replace(product1, id=0, name="Product 2", total_amount=Decimal(2))
        product2_id = uow.products.create(product2)

        result = uow.products.filter(
            supplier_id=supplier_id,
            retailer_id=retailer_id,
            offset=0,
            limit=1,
        )
        assert len(result) == 2
        assert result[0] == 2
