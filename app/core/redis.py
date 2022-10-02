import redis

from app.core.settings import settings
from app.utils.singleton import singleton
from typing import Any


@singleton
class RedisCls:
    def __init__(self):
        pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.client = redis.Redis(connection_pool=pool)

    def set(self, key: str, value: Any, expired: int) -> None:
        self.client.set(key, value, expired)

    def get(self, key: str) -> Any:
        return self.client.get(key)
