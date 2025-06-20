"""Application settings for the backend."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///data.db"


settings = Settings()
