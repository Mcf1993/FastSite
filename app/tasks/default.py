from app.core.celery_config import app
from app.core.celery_config import DBTask
from app.curd.auth.user import user_curd


@app.task(base=DBTask)
def test_query():
    instance = user_curd.get_user_instance_by_username(test_query.db, 'string')
    print(instance)
    return 'success'
