from dependency_injector import containers, providers
from passlib.context import CryptContext

from app.factories.activity_message import ActivityMessageFactory
from app.messagebus import MessageBus
from app.resources.database import init_db
from app.resources.s3_client import init_s3
from app.repos.uow import UnitOfWork
from app.services.images import ImagesService
from app.use_cases.add_payment import AddPayment
from app.use_cases.add_product import AddProduct
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
    s3_client = providers.Resource(init_s3, region=config.aws_region)

    message_bus = providers.Singleton(MessageBus)

    activity_message_factory = providers.Singleton(ActivityMessageFactory)

    images_service = providers.Singleton(
        ImagesService,
        s3_client=s3_client,
        s3_bucket=config.s3_bucket,
        key_prefix="products",
        thumb_size=320,
    )

    uow = providers.Singleton(UnitOfWork, db=db)

    add_payment = providers.Factory(AddPayment, uow=uow)
    add_product = providers.Factory(AddProduct, uow=uow)
    reset_password = providers.Factory(
        SetPassword,
        uow=uow,
        crypt_context=crypt_context,
    )
