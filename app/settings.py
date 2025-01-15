import os

from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV_MAP = {
    "development": ".env",
    "test": ".env.test",
    "production": None,
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    secret_key: str = "9059e1e89b15c9211cc9634c440223b9035a7b2da481da7114a92601261d7375"

    db_uri: str = "postgresql://gold_ledger:secret@127.0.0.1:5432/gold_ledger"


def load_settings() -> Settings:
    env = os.environ.get("ENV", "development")

    return Settings(_env_file=DOTENV_MAP[env])
