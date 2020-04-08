from common.instance import celery
from common.utils import Logger
from missions.model import Missionary, Mission
from missions.engine import MissionaryEngine
# from schedule.interface import drop_all, mission_id_to_entry, add_missionary

log = Logger('mission interface')


def get_valid_mission_id_line():
    return Mission.get_valid_mission_id_line()


def get_valid_missions():
    return Mission.get_valid_missions()


def get_valid_mission_missionary():
    result = []
    mission_id_to_missionary = Missionary.get_valid_mission_id_to_missionary()
    mission_line = Mission.get_valid_missions()
    log.info('all valid mission: {}'.format(tuple(mission_line)))
    for mission in mission_line:
        missionary = mission_id_to_missionary.get(mission.id, None)
        if missionary:
            if mission.is_valid:
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


def do_run_mission(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    if not mission.is_valid:
        return False

    missionary = Missionary.get_or_create_by_mission(mission)
    mission_engine = MissionaryEngine(mission, missionary)
    return mission_engine.try_pass()


# def add_all_missionary(save=True):
#     drop_all()
#     for mission_dict in get_valid_mission_missionary():
#         mission = mission_dict['mission']
#         missionary = mission_dict['missionary']
#         add_missionary(mission.id, run_time=missionary.run_time, save=save)
#     log.info('after add all missionary, the mission id to entry: {}'.format(mission_id_to_entry))


@celery.task(name='mission.run_mission')
def run_mission(mission_id):
    return do_run_mission(mission_id)


# add_all_missionary(save=False)