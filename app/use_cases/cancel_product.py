from fastapi import HTTPException, status

from app.models import User
from app.repos.uow import UnitOfWork


class CancelProduct:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, user: User, product_id: int):
        with self._uow:
            product = self._uow.products.by_id(product_id)

            if not product or product.supplier_id != user.supplier_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="The product was not found",
                )

            product = product.cancel(user)
            self._uow.products.update(product)
