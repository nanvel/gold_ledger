from dependency_injector import containers, providers
from passlib.context import CryptContext

from app.resources.database import init_db
from app.resources.s3_client import init_s3
from app.repos.uow import UnitOfFork
from app.services.images import ImagesService
from app.use_cases.reset_password import ResetPassword


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.routers.auth",
            "app.api.routers.images",
            "app.api.routers.me",
            "app.api.routers.password",
            "app.api.routers.products",
            "app.api.routers.register",
            "app.api.routers.retailer",
            "app.api.routers.retailers",
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

    images_service = providers.Singleton(
        ImagesService,
        s3_client=s3_client,
        s3_bucket=config.s3_bucket,
        key_prefix="products",
        thumb_size=320,
    )

    uow = providers.Singleton(UnitOfFork, db=db)

    reset_password = providers.Factory(
        ResetPassword,
        uow=uow,
        crypt_context=crypt_context,
    )
