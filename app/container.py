from dependency_injector import containers, providers
from passlib.context import CryptContext

from app.resources.database import init_db
from app.repos.uow import UnitOfFork
from app.use_cases.create_user import CreateUser
from app.use_cases.reset_password import ResetPassword


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.routers.auth",
            "app.api.routers.me",
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

    uow = providers.Singleton(UnitOfFork, db=db)

    create_user = providers.Factory(
        CreateUser,
        uow=uow,
        crypt_context=crypt_context,
    )
    reset_password = providers.Factory(
        ResetPassword,
        uow=uow,
        crypt_context=crypt_context,
    )
