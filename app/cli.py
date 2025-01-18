import typer
import uvicorn

from app.container import Container
from app.models import UserRole
from app.settings import load_settings

app = typer.Typer()


class _Container:
    def __init__(self):
        self._container = Container()
        self._container.config.from_dict(load_settings().model_dump())

    def __enter__(self):
        self._container.init_resources()
        return self._container

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._container.shutdown_resources()


@app.callback()
def callback():
    """Gold Ledger."""


@app.command()
def dev_server():
    uvicorn.run(
        app="app.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


@app.command()
def create_admin(username: str, password: str):
    with _Container() as container:
        user = container.create_user()(
            username=username,
            password=password,
            role=UserRole.ADMIN.value,
        )
        typer.echo(user)


@app.command()
def reset_password(username: str, password: str):
    with _Container() as container:
        user = container.reset_password()(
            username=username,
            password=password,
        )
        typer.echo(user)
