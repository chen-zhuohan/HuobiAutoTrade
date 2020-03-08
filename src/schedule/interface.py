from redbeat import RedBeatSchedulerEntry

from common.instance import celery, redis
from common.time_helper import RUN_TIME_SCHEDULE
from missions.interface import get_valid_mission_missionary


def add_missionary(name: str, task: str, run_time: str, args):
    interval = RUN_TIME_SCHEDULE[run_time]
    entry = RedBeatSchedulerEntry(name, task, interval, args=args, app=celery)
    entry.save()


def del_missionary(task_name):
    redis.delete('redbeat:{}'.format(task_name))


def update_missionary(missionary):
    name = 'mission-{}'.format(missionary.mission_id)
    interval = RUN_TIME_SCHEDULE[missionary.run_time]
    entry = RedBeatSchedulerEntry(name, 'mission.run_mission', interval, args=(missionary.mission_id, ), app=celery)
    entry.save()


def add_all_missionary():
    for mission_dict in get_valid_mission_missionary():
        mission = mission_dict['mission']
        missionary = mission_dict['missionary']
        add_missionary('mission-{}'.format(mission.id), 'mission.run_mission', run_time=missionary.run_time,
                       args=(mission.id,))