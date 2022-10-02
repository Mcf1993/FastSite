import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv(verbose=True)


class Settings(BaseSettings):
    TITLE: str = 'FastSite'
    VERSION: str = '1.0.0'
    DEBUG: bool = os.getenv('PY_ENV') == 'Development'
    APP_SECRET_KEY: str = os.getenv('APP_SECRET_KEY')
    APP_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DOCS_URL: str = '/docs'
    DOCUMENTATION_URL: str = '/documentation'
    # DB
    DB_ENGINE: str = os.getenv('DB_ENGINE')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_NAME: str = os.getenv('DB_NAME')
    # Redis
    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: int = os.getenv('REDIS_PORT')
    REDIS_DB: int = os.getenv('REDIS_DB')


settings = Settings()
