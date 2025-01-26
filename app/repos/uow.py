from .images import ImagesRepo
from .payments import PaymentsRepo
from .products import ProductsRepo
from .retailers import RetailersRepo
from .suppliers import SuppliersRepo
from .users import UsersRepo


class UnitOfFork:
    images: ImagesRepo
    payments: PaymentsRepo
    products: ProductsRepo
    retailers: RetailersRepo
    suppliers: SuppliersRepo
    users: UsersRepo

    def __init__(self, db):
        self._db = db
        self._session = None

    def __enter__(self):
        self._session = self._db()
        self.images = ImagesRepo(self._session)
        self.payments = PaymentsRepo(self._session)
        self.products = ProductsRepo(self._session)
        self.retailers = RetailersRepo(self._session)
        self.suppliers = SuppliersRepo(self._session)
        self.users = UsersRepo(self._session)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()

        self._session.close()
