import os
from dotenv import load_dotenv


load_dotenv(verbose=True)

workers = 2
threads = 2
bind = f'{os.getenv("HOST")}:{os.getenv("PORT")}'
daemon = 'false'
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 2000
pidfile = './gunicorn.pid'
loglevel = 'info'
reload = os.getenv("PY_ENV") == "Development"
accesslog = '-'
