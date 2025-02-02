from dataclasses import replace
from datetime import date
from decimal import Decimal

from app.models import Payment, PaymentType, Product, Retailer, Supplier, User
from app.repos.payments import PaymentsRepo
from app.repos.products import ProductsRepo
from app.repos.retailers import RetailersRepo
from app.repos.suppliers import SuppliersRepo
from app.repos.users import UsersRepo
from app.services.accounting import Accounting


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
    )
    payment_id = PaymentsRepo(session).create(payment)

    return supplier_user_id, supplier_id, retailer_id


def test_accounting(session):
    user_id, supplier_id, retailer_id = create_records(session)

    accounting = Accounting(session)
    retailers = accounting._get_retailers(supplier_id)
    assert retailers == [(retailer_id, "Retailer")]

    suppliers = accounting._get_suppliers(retailer_id)
    assert suppliers == [(supplier_id, "Supplier")]

    products = accounting._products_for_supplier(
        supplier_id,
        payment_type=PaymentType.CASH,
    )
    assert len(products) == 1

    payments = accounting._payments_for_retailer(
        retailer_id,
        payment_type=PaymentType.CASH,
    )
    assert len(payments) == 0

    payments = accounting._payments_for_retailer(
        retailer_id,
        payment_type=PaymentType.FINE,
    )
    assert payments == [(supplier_id, Decimal("0.95"))]

    result = accounting.for_supplier(supplier_id, date(2020, 1, 1))

    assert result == {
        retailer_id: {
            "cash": {
                "products": Decimal("1"),
                "confirmed": 0,
                "pending": 0,
                "sum": Decimal("-1"),
                "due_tomorrow_or_later": Decimal("1"),
                "due_today_or_later": Decimal("1"),
                "overdue": Decimal("0"),
                "due_today": Decimal("0"),
            },
            "name": "Retailer",
        }
    }

    result = accounting.for_supplier(supplier_id, date(2021, 1, 1))

    assert result == {
        retailer_id: {
            "cash": {
                "products": Decimal("1"),
                "confirmed": 0,
                "pending": 0,
                "sum": Decimal("-1"),
                "due_tomorrow_or_later": 0,
                "due_today_or_later": Decimal("1"),
                "overdue": 0,
                "due_today": Decimal("1"),
            },
            "name": "Retailer",
        }
    }

    result = accounting.for_supplier(supplier_id, date(2021, 1, 2))

    assert result == {
        retailer_id: {
            "cash": {
                "products": Decimal("1"),
                "confirmed": 0,
                "pending": 0,
                "sum": Decimal("-1"),
                "due_tomorrow_or_later": 0,
                "due_today_or_later": 0,
                "overdue": Decimal("1"),
                "due_today": Decimal("0"),
            },
            "name": "Retailer",
        }
    }

    result = accounting.for_retailer(retailer_id, date(2021, 1, 2))

    assert result == {
        supplier_id: {
            "cash": {
                "products": Decimal("1"),
                "confirmed": 0,
                "pending": 0,
                "sum": Decimal("-1"),
                "due_tomorrow_or_later": 0,
                "due_today_or_later": 0,
                "overdue": Decimal("1"),
                "due_today": Decimal("0"),
            },
            "name": "Supplier",
        }
    }
