from dataclasses import replace
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import sessionmaker

from app.models import (
    Cache,
    DuePayment,
    Payment,
    PaymentType,
    Product,
    Retailer,
    Supplier,
    User,
)
from app.repos.payments import PaymentsRepo
from app.repos.products import ProductsRepo
from app.repos.retailers import RetailersRepo
from app.repos.suppliers import SuppliersRepo
from app.repos.users import UsersRepo
from app.services.accounting import AccountingService


def create_records(session):
    supplier_user = User(
        id=0,
        name="Supplier User",
        username="supplier@mail.com",
        password_hash="password",
        token_version=0,
        retailer_id=None,
        supplier_id=None,
    )
    supplier_user_id = UsersRepo(session).create(supplier_user)
    supplier = Supplier(id=0, name="Supplier", owner_id=supplier_user_id)
    supplier_id = SuppliersRepo(session).create(supplier)
    supplier_user = replace(supplier_user, id=supplier_user_id, supplier_id=supplier_id)
    UsersRepo(session).update(supplier_user)

    retailer_user = User(
        id=0,
        name="Retailer User",
        username="retailer@mail.com",
        password_hash="password",
        token_version=0,
        retailer_id=None,
        supplier_id=None,
    )
    retailer_user_id = UsersRepo(session).create(retailer_user)
    retailer = Retailer(id=0, name="Retailer", owner_id=retailer_user_id)
    retailer_id = RetailersRepo(session).create(retailer)
    retailer_user = replace(retailer_user, id=retailer_user_id, retailer_id=retailer_id)

    retailer2 = Retailer(id=0, name="Retailer 2", owner_id=retailer_user_id)
    retailer2_id = RetailersRepo(session).create(retailer2)

    supplier2 = Supplier(id=0, name="Supplier 2", owner_id=supplier_user_id)
    supplier2_id = SuppliersRepo(session).create(supplier2)

    product = Product(
        id=0,
        name="Product",
        date=date(2021, 1, 1),
        weight=Decimal(1),
        quality=Decimal(1),
        rate=Decimal(1),
        payment_type=PaymentType.CASH,
        payment_amount=Decimal(1),
        payment_weight=None,
        payment_quality=None,
        payment_due_date=date(2021, 1, 1),
        supplier_id=supplier_id,
        retailer_id=retailer_id,
        creator_id=supplier_user_id,
        confirmed_by=retailer_user_id,
        rejected_by=None,
        cancelled_by=None,
    )
    ProductsRepo(session).create(product)

    payment = Payment(
        id=0,
        type=PaymentType.FINE,
        date=date(2021, 1, 1),
        amount=None,
        weight=Decimal(1),
        quality=Decimal(95),
        supplier_id=supplier_id,
        retailer_id=retailer_id,
        creator_id=retailer_user_id,
        confirmed_by=supplier_user_id,
        rejected_by=None,
        cancelled_by=None,
        note=None,
    )
    payment_id = PaymentsRepo(session).create(payment)

    return supplier_user_id, supplier_id, retailer_id


def test_accounting_service(conn):
    session = sessionmaker(bind=conn)()
    user_id, supplier_id, retailer_id = create_records(session)

    accounting = AccountingService(conn)
    result = accounting.compute(supplier_id, retailer_id)

    print(result)

    assert result == Cache(
        supplier_id=supplier_id,
        retailer_id=retailer_id,
        cash_products=Decimal("1"),
        cash_payments=Decimal("0"),
        rtgs_products=Decimal("0"),
        rtgs_payments=Decimal("0"),
        fine_products=Decimal("0"),
        fine_payments=Decimal("0.95000000000000000000"),
        due_payments=[
            DuePayment(
                type=PaymentType.CASH,
                date=date(2021, 1, 1),
                amount=Decimal("1"),
            )
        ],
    )
