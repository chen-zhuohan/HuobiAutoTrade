from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from celery import Celery
from redis import Redis


app = Flask(__name__)
app.config.from_pyfile('../configs.py')
print(app.config)
db = SQLAlchemy(app=app)
redis = Redis.from_url(app.config['REDIS_URL'])
log = logging.getLogger('HuoBi')


# todo config not value
celery = Celery(app.import_name)
celery.conf.update(app.config)
TaskBase = celery.Task
class ContextTask(TaskBase):
    abstract = True
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)
celery.Task = ContextTask