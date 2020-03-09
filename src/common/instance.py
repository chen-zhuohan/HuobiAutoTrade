from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
import logging
from celery import Celery
from redis import Redis

from configs import CeleryConfig


app = Flask(__name__)
app.config.from_pyfile('../configs.py')
for key, value in app.config.items():
    print(key, '\t', value)


db = SQLAlchemy(app=app)
admin = Admin(app, name='火币自动交易', template_mode='bootstrap3')
redis = Redis.from_url(app.config['REDIS_URL'])
log = logging.getLogger('HuoBi')


# todo config not value
celery = Celery(app.import_name)
celery.config_from_object(CeleryConfig)
TaskBase = celery.Task
class ContextTask(TaskBase):
    abstract = True
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)
celery.Task = ContextTask