import os

from app.db.postgresql import SessionLocal
from celery import Celery, Task
from dotenv import load_dotenv


load_dotenv(verbose=True)


app = Celery(
    'fastsite-celery',
    broker=os.getenv('CELERY_BROKER_URL'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND'),
    include=['app.tasks.default']
)


class DBTask(Task):
    """
    自定义任务类添加db连接和关闭。
    使用方式为：通过db属性调用
    """
    _db = None

    def run(self, *args, **kwargs):
        pass

    def after_return(self, *args, **kwargs):
        # 任务执行完成
        if self._db is not None:
            self._db.close()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # 任务失败
        if self._db is not None:
            self._db.close()

    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db
