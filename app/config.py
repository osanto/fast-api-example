import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = os.getenv("ENV_FILE", ".env.local")
        env_file_encoding = "utf-8"

settings = Settings()