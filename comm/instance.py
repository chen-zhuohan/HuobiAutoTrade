from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from celery import Celery


app = Flask(__name__)
app.config.from_pyfile('/project/huobi_trade/configs.py')

db = SQLAlchemy(app=app)
migrate = Migrate(app, db)



log = logging.getLogger('HuoBi')


celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
TaskBase = celery.Task
class ContextTask(TaskBase):
    abstract = True
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)
celery.Task = ContextTask