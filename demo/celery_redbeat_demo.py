from celery import Celery
from celery.schedules import schedule, crontab, solar
from redbeat import RedBeatSchedulerEntry

import configs

celery = Celery(__name__)
celery.config_from_object(configs)


@celery.task
def my_add(a, b):
    result = a + b
    print('{} + {} = {}'.format(a, b, result))
    return result


@celery.task
def my_subtraction(a, b):
    result = a - b
    print('{} - {} = {}'.format(a, b, result))
    return result


interval = schedule(run_every=5)  # seconds
cron = crontab()
entry = RedBeatSchedulerEntry('my_add', '{}.my_add'.format(__name__), interval, args=[5, 2], app=celery)
entry.save()

interval = schedule(run_every=5)  # seconds
entry = RedBeatSchedulerEntry('my_subtraction', 'celery_redbeat_demo.my_subtraction', interval, args=[5, 2], app=celery)
entry.save()