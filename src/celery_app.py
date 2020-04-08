from common.instance import celery
from common.time_helper import RUN_TIME_SCHEDULE
from common.utils import Logger
from missions.interface import run_mission, get_valid_mission_missionary

log = Logger('MY APS')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每十分钟执行test('hello')
    for mission_dict in get_valid_mission_missionary():
        mission = mission_dict['mission']
        missionary = mission_dict['missionary']
        run_time = RUN_TIME_SCHEDULE[missionary.run_time]
        sender.add_periodic_task(run_time, run_mission.s(mission.id), name='mission-{}'.format(mission.id))
    log.info('after add all missionary, the mission id to entry: {}')
