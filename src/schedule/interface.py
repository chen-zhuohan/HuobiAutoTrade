from redbeat import RedBeatSchedulerEntry
from common.instance import celery
from celery.schedules import schedule

from common.instance import redis


def add_missionary():
    interval = schedule(run_every=5)  # seconds
    entry = RedBeatSchedulerEntry('my_subtraction', 'celery_redbeat_demo.my_add', interval, args=[5, 2], app=celery)
    entry.save()


def del_missionary(task_name):
    redis.delete('redbeat:{}'.format(task_name))


def update_missionary(missionary):
    pass