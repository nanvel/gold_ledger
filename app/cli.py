import typer
import uvicorn

from app.container import Container
from app.models import UserRole
from app.settings import load_settings

app = typer.Typer()


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
    container = Container()
    container.config.from_dict(load_settings().model_dump())
    container.init_resources()

    try:
        user = container.create_user()(
            username=username,
            password=password,
            role=UserRole.ADMIN.value,
        )
        print(user)
    finally:
        container.shutdown_resources()


@app.command()
def reset_password(username: str, password: str):
    container = Container()
    container.config.from_dict(load_settings().model_dump())
    container.init_resources()

    try:
        user = container.reset_password()(
            username=username,
            password=password,
        )
        print(user)
    finally:
        container.shutdown_resources()
