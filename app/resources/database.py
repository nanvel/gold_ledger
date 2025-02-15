import logging
from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from sqlalchemy import create_engine, orm

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_uri: str):
        self._engine = create_engine(db_uri)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[orm.Session]]:
        session: orm.Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
