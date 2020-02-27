from uuid import uuid4 as uuid

from common.model_help import save_many_models
from common.test_helper import BaseTest, truncate_all
from missions.engine import MissionaryEngine
from missions.interface import get_valid_mission_missionary, do_run_mission, get_valid_mission_id_line
from missions.model import Missionary, Mission


class Test(BaseTest):
    def create_not_valid_mission(self, ):
        return Mission(name='not valid {}'.format(uuid().hex), target=0, task_line=[-2, -3, -4], run_time=0, is_valid=False)

    def create_valid_mission(self, ):
        return Mission(name=uuid().hex, target=0, task_line=[0, 0, 0, 0], run_time=0,
                       can_run_before_each_task='always_true',
                       can_run_before_target='always_true')

    def create_can_not_run_before_each_task_mission(self, ):
        return Mission(name=uuid().hex, target=0, task_line=[0, -10], run_time=0,
                       can_run_before_each_task='always_false')

    def create_can_run_before_each_task_mission(self):
        return Mission(name=uuid().hex, target=0, task_line=[0, -10], run_time=0,
                       can_run_before_each_task='always_true')

    def create_is_end_missionary(self, mission_id):
        return Missionary(mission_id=mission_id, is_end=True)

    def create_not_end_missionary(self, mission_id):
        return Missionary(mission_id=mission_id)

    def test_get_valid_mission_missionary(self, ):
        """ 测试mission.interface.get_valid_mission_missionary() 是否可以正确筛选可用的mission以及missionary"""
        not_valid_mission = self.create_not_valid_mission()
        valid_mission = self.create_valid_mission()
        save_many_models(not_valid_mission, valid_mission)

        is_end_missionary_valid = self.create_is_end_missionary(valid_mission.id)
        is_end_missionary_not_valid = self.create_is_end_missionary(not_valid_mission.id)
        not_end_missionary_valid = self.create_not_end_missionary(valid_mission.id)
        not_end_missionary_not_valid = self.create_not_end_missionary(not_valid_mission.id)
        save_many_models(is_end_missionary_valid, is_end_missionary_not_valid,
                         not_end_missionary_valid, not_end_missionary_not_valid)

        result = get_valid_mission_missionary()
        for d in result:
            assert d['mission'].is_valid is True
            assert d['mission'].id == valid_mission.id
            assert d['missionary'].is_end is False
            assert d['missionary'].id == not_end_missionary_valid.id

    def test_auto_create_missionary(self, ):
        """ 测试mission.interface.get_valid_mission_missionary() 是否可以根据mission创建不存在的missionary """
        not_valid_mission = self.create_not_valid_mission()
        valid_mission = self.create_valid_mission()
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

    def test_can_not_run_before_each_task(self, ):
        """ 测试mission.MissionaryEngine.can_run_before_each_task() 不过的时候是否为False """
        can_not_run_before_each_task_mission = self.create_can_not_run_before_each_task_mission()
        can_not_run_before_each_task_missionary = self.create_not_end_missionary(can_not_run_before_each_task_mission.id)

        mission_engine = MissionaryEngine(can_not_run_before_each_task_mission, can_not_run_before_each_task_missionary)
        assert mission_engine.can_run_before_each_task() is False

    def test_can_run_before_each_task(self, ):
        """ 测试mission.MissionaryEngine.can_run_before_each_task() 过的时候是否为True """
        can_not_run_before_each_task_mission = self.create_can_run_before_each_task_mission()
        can_not_run_before_each_task_missionary = self.create_not_end_missionary(can_not_run_before_each_task_mission.id)
        save_many_models(can_not_run_before_each_task_mission, can_not_run_before_each_task_missionary)

        mission_engine = MissionaryEngine(can_not_run_before_each_task_mission, can_not_run_before_each_task_missionary)
        assert mission_engine.can_run_before_each_task() is True

    def test_all_pass(self):
        """ 测试mission.MissionaryEngine能否正常通过所有的task """
        mission = self.create_valid_mission()
        missionary = self.create_not_end_missionary(mission.id)
        save_many_models(mission, missionary)

        mission_engine = MissionaryEngine(mission, missionary)
        assert mission_engine.try_pass() is True

    def test_get_valid_mission_id_line(self):
        """ 测试mission.interface.get_valid_mission_id_line() 是否可以正确筛选所有可用的mission id """
        truncate_all()
        not_valid_mission = self.create_not_valid_mission()
        valid_mission = self.create_valid_mission()
        save_many_models(not_valid_mission, valid_mission)

        mission_id_line = get_valid_mission_id_line()
        valid_mission_line = Mission.query.filter_by(is_valid=True).all()
        assert len(mission_id_line) == len(valid_mission_line)

        for mission in valid_mission_line:
            assert mission.id in mission_id_line

    def test_do_run_mission(self):
        """ 测试mission.interface.do_run_mission() 是否可以正常工作，包括自动创建，is not valid返回 """
        truncate_all()
        mission = self.create_valid_mission()
        mission.save()
        assert do_run_mission(mission.id) is True
        mission.is_valid = False
        mission.save()
        assert do_run_mission(mission.id) is False


if __name__ == '__main__':
    import pytest
    pytest.main(['./test.py'])