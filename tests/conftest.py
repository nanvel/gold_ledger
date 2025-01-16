import json
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.app import create_app
from app.container import Container
from app.resources.database import init_db
from app.settings import load_settings

os.environ["ENV"] = "test"


class Data:
    def __init__(self, root: str):
        self.root = root

    def rel(self, *p):
        return os.path.join(self.root, "data", *p)

    def load_json(self, path):
        with open(self.rel(path)) as f:
            return json.load(f)


@pytest.fixture(scope="session")
def data():
    return Data(root=os.path.dirname(os.path.realpath(__file__)))


@pytest.fixture
def session_factory():
    settings = load_settings()

    engine = create_engine(settings.db_uri)
    with engine.connect() as connection:
        with connection.begin_nested() as transaction:
            session_factory = sessionmaker(bind=connection)
            yield session_factory
            transaction.rollback()


@pytest.fixture
def session(session_factory):
    session = session_factory()
    yield session
    session.close()


@pytest.fixture
def container(session_factory):
    container = Container()

    container.config.from_dict(load_settings().model_dump())
    assert "test" in container.config()["db_uri"]

    with container.db.override(session_factory):
        yield container


@pytest.fixture
def http_client(container):
    app = create_app(container)
    yield TestClient(app)
