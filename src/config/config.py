# This file contains env configurations for the application

from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    """ This class contains env variables for the application """
    
    # Application environment variables - Main App
    base_path: str = ""
    cors_origins: str = "http://localhost,http://localhost:3000"
    allowed_methods: List[str] = ['GET','PUT','POST','DELETE']
    bind_ip:str =  "0.0.0.0"
    port: int = 8000
    ssl_cert: str = None
    ssl_key: str = None
    
    # Application environment variables - DataBase
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_username: str = ""
    mongo_password: str = ""
    db_name: str = "task_application"
    
    @classmethod
    def get_settings(cls):
        """ Method to access all setting variables """

        return Settings()