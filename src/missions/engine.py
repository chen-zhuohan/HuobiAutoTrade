from common.email_helper import send_missionary_pass
from common.instance import redis, db
from common.model_help import save_many_models
from common.time_helper import can_run_at_now
from common.utils import Logger
from conditions.interface import get_condition_by_name
from missions.model import Mission, Missionary
from schedule.interface import update_missionary, del_missionary, add_missionary
from tasks.interface import get_task_by_id


class MissionaryEngine:
    log = Logger('Missionary Engine')

    def __init__(self, mission: Mission, missionary: Missionary):
        self.mission_id = mission.id
        self.name = mission.name
        self.target_task_id = mission.target
        self.task_id_line = mission.task_line
        self.can_run_before_each_task = get_condition_by_name(mission.can_run_before_each_task)
        self.can_run_before_target = get_condition_by_name(mission.can_run_before_target)
        self.next_run_mission_id = mission.next_run_mission
        self.missionary = missionary
        self.log.clue = self.name

    @property
    def target(self):
        if not hasattr(self, '_target'):
            self._target = get_task_by_id(self.target_task_id)
            self.log.info('get target: {}'.format(self._target))
        return self._target

    def try_pass(self):
        self.log.info('try to pass')
        if self.can_run_before_each_task():
            if not self.try_pass_each_task():
                return False
        else:
            self.log.info('cant run any task due to can_run_before_each_task')
            return False

        if self.can_run_before_target():
            if self.try_pass_target():
                return True
        else:
            self.log.info('cant run target due to can_run_before_target')
            return False

    def try_pass_each_task(self):
        for index, task_id in enumerate(self.task_id_line):
            if index < self.missionary.next_task_index:
                continue

            task = get_task_by_id(task_id)
            self.log.info('run from index: {}, task_id {}, get task: {} '.format(index, task_id, task))
            if not self.pass_task(index, task):
                return False

        self.log.info('pass all task successfully')
        return True

    def pass_task(self, index, task) -> bool:
        def _do_run():
            task.get_info_from_mission(index, self)
            can_run_result = task.can_run()
            if can_run_result and task.try_pass():
                self.log.info('pass one task successfully')
                self.missionary.add_task_index(save=False)
                return True
            else:
                self.log.info('task fail at index: {}, can_run: {}'.format(index, can_run_result))
                return False

        if self.missionary.run_time == task.run_time:
            self.log.info('missionary run time is same as task run time')
            return _do_run()

        now_missionary_run_time = self.missionary.run_time
        self.missionary.run_time = task.run_time        # if not same，follow to task
        self.missionary.save()
        self.log.info('missionary run time update to {}'.format(self.missionary.run_time))
        update_missionary(self.missionary)

        if can_run_at_now(task.run_time, now=now_missionary_run_time):
            return _do_run()
        else:
            self.log.info('task({}) cant run at {}'.format(task.run_time, now_missionary_run_time))
            return False

    def try_pass_target(self):
        self.target.get_info_from_mission(mission_engine=self)
        if self.target.can_run() and self.target.try_pass():
            self.log.info('pass target successfully')
            self.missionary.finish()
            self.mission_finish()
            self.log.info('update missionary model successfully')
            send_missionary_pass(self.name)
            return True
        return False

    def mission_finish(self):
        self.log.info('after all pass, ready to start next mission')
        finished_mission = Mission.query.filter_by(id=self.mission_id).first()
        finished_mission.is_valid = False

        mission = Mission.query.filter_by(id=self.next_run_mission_id).first()
        mission.is_valid = True
        save_many_models(finished_mission, mission)
        self.log.info('finished mission: {}, next mission: {}'.format(finished_mission, mission))

        self.log.info('try to del finished mission')
        del_missionary(finished_mission.id)
        missionary = Missionary.get_or_create_by_mission(mission)
        self.log.info('try to add next mission')
        add_missionary(mission_id=mission.id, run_time=missionary.run_time)

    @property
    def next_task_index(self):
        redis.set()
    # def show_info(self):
    #     result = []
    #     for task_id in self.task_id_line:
    #         result.append(task().pass_(True))
    #     return result

#     def get_last_finished_task_id(self) -> int:
#         # 如果一条都找不到，或找到的已经is end=True，创建一条-1，否则返回正常值
#         start = time.time()
#         self.log.info('try to get_last_finished_task_id')
#         result = TaskPass.get_last(mission=self.NAME)
#         if result is None or result.is_end:
#             self.log.info('first run, result: {}'.format(result))
#             self.create_first_record()
#             return -1
#
#         self.start_time = result.mission_start
#         self.log.info('get_last_finished_task_id cost {}'.format(time.time() - start))
#         return result.task_id
#
#     def create_first_record(self):
#         self.start_time = now_format_time()
#         tp = TaskPass(mission_start=self.start_time, mission=self.NAME, task_id=-1)
#         tp.save()
#         self.log.info('create first recode, task pass: {}'.format(tp))
#
#     def save_pass_record(self, task):
#         if getattr(self, 'start_time', False):
#             mp = TaskPass(task=task.__class__.__name__,
#                           mission_start=self.start_time,
#                           mission=self.NAME,
#                           task_id=self.TASKLINE.index(task))
#             if mp.task_id == len(self.TASKLINE) - 1:
#                 mp.is_end = True
#             mp.save()
#         else:
#             self.create_first_record()
#
#     @classmethod
#     def run(cls):
#         if cls.can_run:
#             m = cls()
#             m.do_run()
#             return m
#         else:
#             raise Exception('cant run')
#
#     @property
#     def can_run(self):
#         return not Conditions.query.filter_by(valid=True).exists()
#
#     def do_run(self):
#         raise Exception('must be covered')
#
#
# class MissionForBuy(MissionBase):
#     Trade = None
#
#     def __init__(self, *args, **kwargs):
#         self.check_pre_init()
#         super().__init__(*args, **kwargs)
#
#     def check_pre_init(self):
#         if self.Trade is None:
#             raise Exception('Trade should not be None')
#
#     def do_run(self):
#         self.log.info('mission.start')
#         start = time.time()
#         if self.pass_():
#             order = self.Trade(self.NAME).buy()
#             trade = Trade.create_by_order(order, self.NAME)
#             send_trade('成功买入!', trade)
#         self.log.info('MissionForBuy.run cost {}'.format(time.time() - start))
#
#
# class MissionForSell(MissionBase):
#     Trade = None
#
#     def __init__(self, *args, **kwargs):
#         self.check_pre_init()
#         super().__init__(*args, **kwargs)
#
#     def check_pre_init(self):
#         if self.Trade is None:
#             raise Exception('Trade should not be None')
#
#     def do_run(self):
#         if self.pass_():
#             order = self.Trade(self.NAME).sell()
#             trade = Trade.create_by_order(order, self.NAME)
#             send_trade('成功卖出!', trade)