from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal
from typing import Optional

from .payment_status import PaymentStatus
from .payment_type import PaymentType
from .user import User


@dataclass(frozen=True)
class Product:
    id: int
    name: str
    date: date
    weight: Decimal
    quality: Decimal
    rate: Decimal
    payment_type: PaymentType
    payment_amount: Optional[Decimal]
    payment_weight: Optional[Decimal]
    payment_quality: Optional[Decimal]
    payment_due_date: date
    supplier_id: int
    retailer_id: int
    creator_id: int
    confirmed_by: Optional[int]
    rejected_by: Optional[int]
    cancelled_by: Optional[int]

    @property
    def status(self) -> PaymentStatus:
        if self.confirmed_by is not None:
            return PaymentStatus.CONFIRMED
        if self.rejected_by is not None:
            return PaymentStatus.REJECTED
        if self.cancelled_by is not None:
            return PaymentStatus.CANCELED
        return PaymentStatus.PENDING

    def confirm(self, user: User):
        assert self.confirmed_by is None
        assert self.rejected_by is None
        assert self.cancelled_by is None
        assert user.retailer_id == self.retailer_id
        return replace(self, confirmed_by=user.id)

    def reject(self, user: User):
        assert self.confirmed_by is None
        assert self.rejected_by is None
        assert self.cancelled_by is None
        assert user.retailer_id == self.retailer_id
        return replace(self, rejected_by=user.id)

    def cancel(self, user: User):
        assert self.confirmed_by is None
        assert self.rejected_by is None
        assert self.cancelled_by is None
        assert user.supplier_id == self.supplier_id
        return replace(self, cancelled_by=user.id)

    def validate(self):
        if self.payment_type == PaymentType.FINE:
            if self.payment_amount is not None:
                raise ValueError("Amount is not required for Fine payment type")
            if self.payment_weight is None:
                raise ValueError("Weight is required for Fine payment type")
            if self.payment_quality is None:
                raise ValueError("Quality is required for Fine payment type")
        else:
            if self.payment_amount is None:
                raise ValueError("Amount is required for Cash payment type")
            if self.payment_weight is not None:
                raise ValueError("Weight is not required for Cash payment type")
            if self.payment_quality is not None:
                raise ValueError("Quality is not required for Cash payment type")
