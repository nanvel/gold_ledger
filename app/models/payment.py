from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal
from typing import Optional

from .payment_type import PaymentType
from .user import User


@dataclass(frozen=True)
class Payment:
    id: int
    type: PaymentType
    date: date
    weight: Optional[Decimal]
    quality: Optional[Decimal]
    amount: Decimal
    supplier_id: int
    retailer_id: int
    creator_id: int
    confirmed_by: Optional[int]
    rejected_by: Optional[int]
    cancelled_by: Optional[int]

    def confirm(self, user: User):
        assert self.confirmed_by is None
        assert self.rejected_by is None
        assert self.cancelled_by is None
        assert user.supplier_id == self.supplier_id
        return replace(self, confirmed_by=user.id)

    def reject(self, user: User):
        assert self.confirmed_by is None
        assert self.rejected_by is None
        assert self.cancelled_by is None
        assert user.supplier_id == self.supplier_id
        return replace(self, rejected_by=user.id)

    def cancel(self, user: User):
        assert self.confirmed_by is None
        assert self.rejected_by is None
        assert self.cancelled_by is None
        assert user.retailer_id == self.retailer_id
        return replace(self, cancelled_by=user.id)

    def validate(self):
        if self.type == PaymentType.FINE:
            assert self.weight is not None
            assert self.quality is not None
            assert self.amount is None
        else:
            assert self.weight is None
            assert self.quality is None
            assert self.amount is not None
