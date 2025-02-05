from tqdm import tqdm

from app.repos.uow import UnitOfWork
from app.services.accounting import AccountingService


class RefreshCache:
    def __init__(self, uow: UnitOfWork, accounting_service: AccountingService):
        self._uow = uow
        self._accounting_service = accounting_service

    def __call__(self):
        with self._uow:
            keys = sorted(self._uow.cache.all_keys())
            for supplier_id, retailer_id in tqdm(keys):
                cache = self._accounting_service.compute(
                    supplier_id=supplier_id,
                    retailer_id=retailer_id,
                )
                self._uow.cache.create_or_update(cache)
