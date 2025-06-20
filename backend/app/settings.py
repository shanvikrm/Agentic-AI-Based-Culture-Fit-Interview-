"""Application settings for the backend."""

import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Environment settings."""

    database_url: str = os.getenv(
        "DATABASE_URL",
        "mongodb://localhost:27017",
    )
    mongo_db_name: str = "culture_fit"


settings = Settings()
