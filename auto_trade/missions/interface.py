from common.instance import celery
from common.utils import Logger
from missions.model import Missionary, Mission
from missions.engine import MissionaryEngine


log = Logger('mission interface')


def get_valid_mission_missionary():
    result = []
    mission_id_to_missionary = Missionary.get_valid_mission_id_to_missionary()
    mission_line = Mission.get_valid_missions()
    for mission in mission_line:
        missionary = mission_id_to_missionary.get(mission.id, None)
        if missionary:
            result.append({
                'mission': mission,
                'missionary': missionary
            })
        else:
            log.info('mission({})\'s missionary not found, create new'.format(mission))
            missionary = Missionary.create_by_mission(mission)
            result.append({
                'mission': mission,
                'missionary': missionary
            })
    log.info('get valid mission missionary: {}'.format(result))
    return result


@celery.task(name='mission.run_missionary')
def run_missionary(mission, missionary):
    mission_engine = MissionaryEngine(mission, missionary)
    mission_engine.try_pass()