from redbeat import RedBeatSchedulerEntry
from celery_redbeat_demo import celery, my_subtraction
from celery.schedules import schedule

from common.instance import redis


def add_mission():
    interval = schedule(run_every=5)  # seconds
    entry = RedBeatSchedulerEntry('my_subtraction', 'celery_redbeat_demo.my_add', interval, args=[5, 2], app=celery)
    entry.save()


def del_mission(task_name):
    redis.delete('redbeat:{}'.format(task_name))