from redbeat import RedBeatSchedulerEntry

from common.instance import celery, redis
from common.time_helper import RUN_TIME_SCHEDULE
from common.utils import Logger


RUNNING_TASK_NAME = 'mission-{}'
mission_id_to_entry = dict()
logger = Logger('scheduler interface')


def get_entry(mission_id, raise_error=False) -> RedBeatSchedulerEntry:
    if mission_id_to_entry.get(mission_id, False):
        return mission_id_to_entry.get(mission_id)
    elif raise_error:
        logger.info('not find the mission id entry, will raise error')
        raise ModuleNotFoundError('the mission has not in schedule, please add the mission first before del and update')


def drop_all():
    keys = redis.keys('redbeat:*')
    [redis.delete(key) for key in keys]
    for entry in mission_id_to_entry.values():
        entry.delete()


def add_missionary(mission_id: int, run_time: str, task: str = 'mission.run_mission'):
    name = RUNNING_TASK_NAME.format(mission_id)
    args = (mission_id,)
    interval = RUN_TIME_SCHEDULE[run_time]

    logger.info('add missionary: mission id: {}, run time: {}'.format(mission_id, interval))
    entry = RedBeatSchedulerEntry(name, task, interval, args=args, app=celery)
    entry.save()
    mission_id_to_entry[mission_id] = entry
    return entry


def del_missionary(mission_id):
    entry = get_entry(mission_id)
    entry.delete()
    logger.info('has delete entry: {}'.format(entry))


def update_missionary(missionary=None, mission=None):
    """ give one of two args """
    if mission is not None:
        from missions.interface import Missionary
        missionary = Missionary.get_or_create_by_mission(mission=mission)

    old_entry = get_entry(missionary.mission_id)
    new_entry = add_missionary(missionary.mission_id, missionary.run_time)
    logger.info('update, the old: {}, the new: {}'.format(old_entry, new_entry))
    return new_entry


def add_all_missionary():
    from missions.interface import get_valid_mission_missionary
    drop_all()
    for mission_dict in get_valid_mission_missionary():
        mission = mission_dict['mission']
        missionary = mission_dict['missionary']
        add_missionary(mission.id, run_time=missionary.run_time)
    logger.info('after add all missionary, the mission id to entry: {}'.format(mission_id_to_entry))