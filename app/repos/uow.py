from .activities import ActivitiesRepo
from .cache import CacheRepo
from .connections import ConnectionsRepo
from .images import ImagesRepo
from .invites import InvitesRepo
from .payments import PaymentsRepo
from .products import ProductsRepo
from .retailers import RetailersRepo
from .suppliers import SuppliersRepo
from .users import UsersRepo


class UnitOfWork:
    activities: ActivitiesRepo
    cache: CacheRepo
    connections: ConnectionsRepo
    images: ImagesRepo
    invites: InvitesRepo
    payments: PaymentsRepo
    products: ProductsRepo
    retailers: RetailersRepo
    suppliers: SuppliersRepo
    users: UsersRepo

    def __init__(self, db):
        self._db = db
        self._session = None

    def __enter__(self):
        self._session = self._db.session().__enter__()
        self.activities = ActivitiesRepo(self._session)
        self.cache = CacheRepo(self._session)
        self.connections = ConnectionsRepo(self._session)
        self.images = ImagesRepo(self._session)
        self.invites = InvitesRepo(self._session)
        self.payments = PaymentsRepo(self._session)
        self.products = ProductsRepo(self._session)
        self.retailers = RetailersRepo(self._session)
        self.suppliers = SuppliersRepo(self._session)
        self.users = UsersRepo(self._session)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.__exit__(exc_type, exc_val, exc_tb)
