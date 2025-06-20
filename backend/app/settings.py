"""Application settings for the backend."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Environment settings."""

    database_url: str = os.getenv(
        "DATABASE_URL",
        "mongodb+srv://vikramshanmugam2002:oQDDiwFyExNZ6b5D@cluster0.kotkjf5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    )
    mongo_db_name: str = "culture_fit"


settings = Settings()
