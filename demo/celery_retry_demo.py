from celery import Celery
from celery.app.task import Task
import time

import configs

celery = Celery(__name__)
celery.config_from_object(configs)


@celery.task(bind=True, name='记录订单', max_retries=3)
def test(self: Task):
    try:
        print(time.time())
        raise Exception('test')
    except Exception as e:
        print('try to record trade fail, detail: {}, retry: {}'.format(e, self.request.retries))
        self.retry(countdown=3, exc=e)


# celery -A celery_retry_demo worker --loglevel=info