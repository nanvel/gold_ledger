from dependency_injector import containers, providers
from passlib.context import CryptContext

from app.message_bus import MessageBus
from app.resources.database import init_db, init_db_readonly
from app.resources.s3_client import init_s3
from app.repos.uow import UnitOfWork
from app.services.accounting import AccountingService
from app.services.images import ImagesService
from app.use_cases.add_payment import AddPayment
from app.use_cases.add_product import AddProduct
from app.use_cases.cancel_payment import CancelPayment
from app.use_cases.cancel_product import CancelProduct
from app.use_cases.confirm_payment import ConfirmPayment
from app.use_cases.confirm_product import ConfirmProduct
from app.use_cases.refresh_cache import RefreshCache
from app.use_cases.reject_payment import RejectPayment
from app.use_cases.reject_product import RejectProduct
from app.use_cases.set_password import SetPassword


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.routers.accounting",
            "app.api.routers.activities",
            "app.api.routers.auth",
            "app.api.routers.images",
            "app.api.routers.me",
            "app.api.routers.payments",
            "app.api.routers.password",
            "app.api.routers.products",
            "app.api.routers.register",
            "app.api.routers.retailers",
            "app.api.routers.staff",
            "app.api.routers.suppliers",
        ]
    )

    jwt_algorithm = providers.Object("HS256")
    crypt_context = providers.Singleton(
        CryptContext,
        schemes=["bcrypt"],
        deprecated="auto",
    )

    db = providers.Resource(init_db, db_uri=config.db_uri)
    db_readonly = providers.Resource(init_db_readonly, db_uri=config.db_uri)
    s3_client = providers.Resource(init_s3, region=config.aws_region)

    images_service = providers.Singleton(
        ImagesService,
        s3_client=s3_client,
        s3_bucket=config.s3_bucket,
        key_prefix="products",
        thumb_size=320,
    )

    uow = providers.Singleton(UnitOfWork, db=db)

    accounting_service = providers.Singleton(AccountingService, db=db_readonly)

    message_bus = providers.Singleton(
        MessageBus,
        uow=uow,
        accounting_service=accounting_service,
    )

    add_payment = providers.Factory(AddPayment, uow=uow, message_bus=message_bus)
    add_product = providers.Factory(AddProduct, uow=uow, message_bus=message_bus)
    cancel_payment = providers.Factory(CancelPayment, uow=uow, message_bus=message_bus)
    cancel_product = providers.Factory(CancelProduct, uow=uow, message_bus=message_bus)
    confirm_payment = providers.Factory(
        ConfirmPayment, uow=uow, message_bus=message_bus
    )
    confirm_product = providers.Factory(
        ConfirmProduct, uow=uow, message_bus=message_bus
    )
    reject_payment = providers.Factory(RejectPayment, uow=uow, message_bus=message_bus)
    reject_product = providers.Factory(RejectProduct, uow=uow, message_bus=message_bus)
    refresh_cache = providers.Factory(
        RefreshCache,
        uow=uow,
        accounting_service=accounting_service,
    )
    reset_password = providers.Factory(
        SetPassword,
        uow=uow,
        crypt_context=crypt_context,
    )
