import json
import os

import pytest
from fastapi.testclient import TestClient

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
def session():
    settings = load_settings()

    for session_factory in init_db(settings.db_uri):
        session = session_factory()
        session.begin_nested()
        yield session
        session.rollback()


@pytest.fixture
def container(session):
    container = Container()
    container.config.from_dict(load_settings().model_dump())

    with container.db.override(lambda: session):
        yield container

    session.rollback()


@pytest.fixture
def http_client(container):
    app = create_app(container)
    yield TestClient(app)
