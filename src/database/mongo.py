import logging
from pymongo import MongoClient
from src.config.config import Settings
class MongoDB:
    """This class defines the mongo connection"""

    settings = Settings.get_settings()
    client = MongoClient(
        host=settings.mongo_host,
        port=settings.mongo_port,
        username=settings.mongo_username,
        password=settings.mongo_password
    )

    db = client[settings.db_name]

    @classmethod
    def get_db_cursor(cls):
        logging.debug(f"Connected to db instance: {cls.settings.mongo_host}")
        return cls.db