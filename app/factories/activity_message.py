from app.models import Activity, ActivityType, PaymentType
from app.repos.uow import UnitOfWork


class ActivityMessageFactory:
    def __init__(self):
        pass

    def from_activity(self, activity: Activity, uow: UnitOfWork) -> str:
        if activity.type == ActivityType.PRODUCT_GIVEN:
            user = uow.users.by_id(activity.user_id)
            product = uow.products.by_id(activity.product_id)
            retailer = uow.retailers.by_id(activity.retailer_id)
            supplier = uow.suppliers.by_id(activity.supplier_id)
            return (
                f"{user.display_name} ({supplier.id}:{supplier.name}) "
                f"has given {product.name} to {retailer.id}:{retailer.name}"
            )
        elif activity.type == ActivityType.PRODUCT_CONFIRMED:
            user = uow.users.by_id(activity.user_id)
            product = uow.products.by_id(activity.product_id)
            retailer = uow.retailers.by_id(activity.retailer_id)
            return f"{user.display_name} ({retailer.id}:{retailer.name}) has received {product.name}"
        elif activity.type == ActivityType.PRODUCT_REJECTED:
            user = uow.users.by_id(activity.user_id)
            product = uow.products.by_id(activity.product_id)
            retailer = uow.retailers.by_id(activity.retailer_id)
            return f"{user.display_name} ({retailer.id}:{retailer.name}) has rejected {product.name}"
        elif activity.type == ActivityType.PAYMENT_ADDED:
            user = uow.users.by_id(activity.user_id)
            payment = uow.payments.by_id(activity.payment_id)
            retailer = uow.retailers.by_id(activity.retailer_id)
            if payment.type == PaymentType.FINE:
                return (
                    f"{user.display_name} ({retailer.id}:{retailer.name}) "
                    f"has added a payment of {payment.weight}g {payment.quality}% ({payment.type.label})"
                )
            else:
                return (
                    f"{user.display_name} ({retailer.id}:{retailer.name}) "
                    f"has added a payment of ₹{payment.amount} ({payment.type.label})"
                )
        elif activity.type == ActivityType.PAYMENT_CONFIRMED:
            user = uow.users.by_id(activity.user_id)
            payment = uow.payments.by_id(activity.payment_id)
            supplier = uow.suppliers.by_id(activity.supplier_id)
            if payment.type == PaymentType.FINE:
                return (
                    f"{user.display_name} ({supplier.id}:{supplier.name}) "
                    f"has confirmed a payment of {payment.weight}g {payment.quality}% ({payment.type.label})"
                )
            else:
                return (
                    f"{user.display_name} ({supplier.id}:{supplier.name}) "
                    f"has confirmed a payment of ₹{payment.amount} ({payment.type.label})"
                )
        elif activity.type == ActivityType.PAYMENT_REJECTED:
            user = uow.users.by_id(activity.user_id)
            payment = uow.payments.by_id(activity.payment_id)
            supplier = uow.suppliers.by_id(activity.supplier_id)
            if payment.type == PaymentType.FINE:
                return (
                    f"{user.display_name} ({supplier.id}:{supplier.name}) "
                    f"has rejected a payment of {payment.weight}g {payment.quality}% ({payment.type.label})"
                )
            return (
                f"{user.display_name} ({supplier.id}:{supplier.name}) "
                f"has rejected a payment of ₹{payment.amount} ({payment.type.label})"
            )
        else:
            raise ValueError(f"Unknown activity type: {activity.type}")
