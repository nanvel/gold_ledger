from app.models import StoreType


def test_store_type():
    assert StoreType.SUPPLIER != StoreType.RETAILER
