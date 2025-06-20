"""MongoDB database connection utilities."""

from pymongo import MongoClient

from .settings import settings

client = MongoClient(settings.database_url)

db = client[settings.mongo_db_name]
