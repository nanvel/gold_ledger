from app.api.app import create_app
from app.container import Container
from app.settings import load_settings


container = Container()
container.config.from_dict(load_settings().model_dump())
app = create_app(container=container)
