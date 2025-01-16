from dependency_injector import containers, providers
from passlib.context import CryptContext

from app.resources.database import init_db
from app.repos.uow import UnitOfFork


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    jwt_algorithm = providers.Object("HS256")
    crypt_context = providers.Singleton(
        CryptContext,
        schemes=["bcrypt"],
        deprecated="auto",
    )

    db = providers.Resource(init_db, db_uri=config.db_uri)

    uow = providers.Singleton(UnitOfFork, db=db)
