from redbeat import RedBeatSchedulerEntry

from common.instance import celery, redis
from common.time_helper import RUN_TIME_SCHEDULE
from common.utils import Logger


RUNNING_TASK_NAME = 'mission-{}'
logger = Logger('scheduler interface')


def add_missionary(mission_id, run_time: str, task: str = 'mission.run_mission'):
    name = RUNNING_TASK_NAME.format(mission_id)
    args = (mission_id,)
    interval = RUN_TIME_SCHEDULE[run_time]
    logger.info('add missionary: mission id: {}, run time: {}'.format(mission_id, interval))
    entry = RedBeatSchedulerEntry(name, task, interval, args=args, app=celery)
    entry.save()


def del_missionary(mission_id):
    redis.delete('redbeat:{}'.format(RUNNING_TASK_NAME.format(mission_id)))


def update_missionary(missionary):
    name = RUNNING_TASK_NAME.format(missionary.mission_id)
    interval = RUN_TIME_SCHEDULE[missionary.run_time]
    entry = RedBeatSchedulerEntry(name, 'mission.run_mission', interval, args=(missionary.mission_id, ), app=celery)
    entry.save()


def add_all_missionary():
    from missions.interface import get_valid_mission_missionary
    for mission_dict in get_valid_mission_missionary():
        mission = mission_dict['mission']
        missionary = mission_dict['missionary']
        logger.info('add mission(id: {}) to redis, run_time: {}'.format(mission.id, missionary.run_time))
        add_missionary(mission.id, run_time=missionary.run_time)