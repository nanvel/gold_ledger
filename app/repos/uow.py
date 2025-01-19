from .products import ProductsRepo
from .retailer_stores import RetailerStoresRepo
from .supplier_stores import SupplierStoresRepo
from .users import UsersRepo


class UnitOfFork:
    products: ProductsRepo
    retailer_stores: RetailerStoresRepo
    supplier_stores: SupplierStoresRepo
    users: UsersRepo

    def __init__(self, db):
        self._db = db
        self._session = None

    def __enter__(self):
        self._session = self._db()
        self._session.begin()
        self.products = ProductsRepo(self._session)
        self.retailer_stores = RetailerStoresRepo(self._session)
        self.supplier_stores = SupplierStoresRepo(self._session)
        self.users = UsersRepo(self._session)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()

        self._session.close()
