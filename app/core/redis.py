import math
import redis
import time
import uuid

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


@singleton
class DistributedLock:
    DISTRIBUTED_KEY = 'DistributedLock:'

    def __init__(self):
        redis_pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        self.redis_client = redis.Redis(connection_pool=redis_pool)

    def acquire_lock_with_timeout(self, lock_name: str, acquire_timeout: int = 3, lock_timeout: int = 3):
        lockname = f'{self.DISTRIBUTED_KEY}{lock_name}'
        lock_timeout = int(math.ceil(lock_timeout))
        end_time = time.time() + acquire_timeout
        identifier = str(uuid.uuid4())
        while time.time() < end_time:
            if self.redis_client.set(lockname, identifier, ex=lock_timeout, nx=True):
                return identifier
            time.sleep(0.001)
        return False

    def release_lock(self, lock_name: str, identifier: str):
        unlock_script = """
        if redis.call("get",KEYS[1]) == ARGV[1] then
            return redis.call("del",KEYS[1])
        else
            return 0
        end
        """
        lock_name = f'{self.DISTRIBUTED_KEY}{lock_name}'
        unlock = self.redis_client.register_script(unlock_script)
        result = unlock(keys=[lock_name], args=[identifier])
        if result:
            return True
        return False
