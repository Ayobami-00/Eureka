import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyHttpUrl
from pydantic.networks import EmailStr

path = Path.cwd()

env_path = path / ".env"

load_dotenv(dotenv_path=env_path)

ENVIRONMENT = os.environ.get("ENVIRONMENT", "DEVELOPMENT")


if ENVIRONMENT == "PRODUCTION":
    """
    set prod environment variables

    """

    db_user: str = os.environ.get("DB_USER", None)
    db_password: str = os.environ.get("DB_PASSWORD", None)
    db_host: str = os.environ.get("DB_HOST", None)
    db_port: str = os.environ.get("DB_PORT", None)
    db_engine: str = os.environ.get("DB_ENGINE", None)
    db_name: str = os.environ.get("DB_NAME", None)


elif ENVIRONMENT == "DEVELOPMENT" or ENVIRONMENT == "LOCAL":
    """
    set dev environment variables

    """
    db_user: str = os.environ.get("DB_USER", None)
    db_password: str = os.environ.get("DB_PASSWORD", None)
    db_host: str = os.environ.get("DB_HOST", None)
    db_port: str = os.environ.get("DB_PORT", None)
    db_engine: str = os.environ.get("DB_ENGINE", None)
    db_name: str = os.environ.get("DB_NAME", None)



else:
    pass


class Settings(BaseSettings):
    """
    Set config variables on settins class

    """
    API_TITLE: str = os.environ.get("API_TITLE", "EUREKA BUSINESS API SERVICE")
    API_ROOT_PATH: str = os.environ.get("API_ROOT_PATH", "/api")
    DB_USER: str = db_user
    DB_PASSWORD: str = db_password
    DB_HOST: str = db_host
    DB_PORT: str = db_port
    DB_ENGINE: str = db_engine
    DATABASE_URI = "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
        db_engine=db_engine,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name,
    )


settings = Settings()
