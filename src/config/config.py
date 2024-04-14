# This file contains env configurations for the application

from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    """ This class contains env variables for the application """
    
    # Application environment variables - Main App
    base_path: str = ""
    cors_origins: str = "http://localhost,http://localhost:8000"
    allowed_methods: List[str] = ['GET','PUT','POST','DELETE']
    bind_ip:str =  "0.0.0.0"
    port: int = 8000
    ssl_cert: str = None
    ssl_key: str = None
    
    # Application environment variables - DataBase
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_username: str = "root"
    mongo_password: str = "example"
    db_name: str = "task_app"

    # User related environment variables
    hash_algorithm: str = "HS256" # you can change your encryption technique for jwt token
    hash_key: str = "put_your_HS256_random_hash_key"
    
    @classmethod
    def get_settings(cls):
        """ Method to access all setting variables """

        return Settings()