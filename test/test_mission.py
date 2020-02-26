from uuid import uuid4 as uuid
from src.common.model_help import save_many_models
from src.missions.engine import MissionaryEngine
from src.missions.interface import get_valid_mission_missionary
from src.missions.model import Missionary, Mission


def create_not_valid_mission():
    return Mission(name='not valid {}'.format(uuid().hex), target=0, task_line=[-2, -3, -4], run_time=0, is_valid=False)


def create_valid_mission():
    return Mission(name=uuid().hex, target=0, task_line=[0, -10], run_time=0,
                   can_run_before_each_task='always_true',
                   can_run_before_target='always_true')


def create_can_not_run_before_each_task_mission():
    return Mission(name=uuid().hex, target=0, task_line=[0, -10], run_time=0,
                   can_run_before_each_task='always_false')


def create_is_end_missionary(mission_id):
    return Missionary(mission_id=mission_id, is_end=True)


def create_not_end_missionary(mission_id):
    return Missionary(mission_id=mission_id)


def test_get_valid_mission_missionary():
    """ 测试mission.interface.get_valid_mission_missionary() 是否可以正确筛选可用的mission以及missionary"""
    not_valid_mission = create_not_valid_mission()
    valid_mission = create_valid_mission()
    save_many_models(not_valid_mission, valid_mission)

    is_end_missionary_valid = create_is_end_missionary(valid_mission.id)
    is_end_missionary_not_valid = create_is_end_missionary(not_valid_mission.id)
    not_end_missionary_valid = create_not_end_missionary(valid_mission.id)
    not_end_missionary_not_valid = create_not_end_missionary(not_valid_mission.id)
    save_many_models(is_end_missionary_valid, is_end_missionary_not_valid,
                     not_end_missionary_valid, not_end_missionary_not_valid)

    result = get_valid_mission_missionary()
    for d in result:
        assert d['mission'].is_valid is True
        assert d['mission'].id == valid_mission.id
        assert d['missionary'].is_end is False
        assert d['missionary'].id == not_end_missionary_valid.id


def test_auto_create_missionary():
    """ 测试mission.interface.get_valid_mission_missionary() 是否可以根据mission创建不存在的missionary"""
    not_valid_mission = create_not_valid_mission()
    valid_mission = create_valid_mission()
    save_many_models(not_valid_mission, valid_mission)
    result = get_valid_mission_missionary()
    has_missionary = False
    wrong = False
    for d in result:
        if d['missionary'].mission_id == valid_mission.id:
            has_missionary = True
        if d['missionary'].mission_id == not_valid_mission.id:
            wrong = True

    assert has_missionary is True
    assert wrong is False


def test_can_not_run_before_each_task():
    can_not_run_before_each_task_mission = create_can_not_run_before_each_task_mission()
    can_not_run_before_each_task_missionary = Missionary.create_by_mission(can_not_run_before_each_task_mission)

    mission_engine = MissionaryEngine(can_not_run_before_each_task_mission, can_not_run_before_each_task_missionary)
    assert mission_engine.can_run_before_each_task() is False