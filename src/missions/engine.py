from common.email_helper import send_missionary_pass
from common.instance import redis
from common.utils import Logger
from conditions.interface import get_condition_by_name
from missions.model import Mission, Missionary
from tasks.interface import get_task_by_id


class MissionaryEngine:
    log = Logger('Missionary Engine')


    def __init__(self, mission: Mission, missionary: Missionary):
        self.name = mission.name
        self.target_task_id = mission.target
        self.task_id_line = mission.task_line
        self.can_run_before_each_task = get_condition_by_name(mission.can_run_before_each_task)
        self.can_run_before_target = get_condition_by_name(mission.can_run_before_target)
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
                return
        else:
            self.log.info('cant run any task due to can_run_before_each_task')
            return

        if self.can_run_before_target():
            if self.try_pass_target():
                return True
        else:
            self.log.info('cant run target due to can_run_before_target')

    def try_pass_each_task(self):
        for index, task_id in enumerate(self.task_id_line):
            if index < self.missionary.next_task_index:
                continue

            self.log.info('run from index: {}, task_id {}'.format(index, task_id))
            task = get_task_by_id(task_id)
            self.log.info('get task: {} '.format(task))
            if task.can_run() and task.passed(self, index):
                self.log.info('pass one task successfully')
                self.missionary.add_next_task_index()
            else:
                self.log.info('task fail at index: {}'.format(index))
                return False

        self.log.info('pass all task successfully')
        return True

    def try_pass_target(self):
        if self.target.can_run() and self.target.passed(self):
            self.log.info('pass target successfully')
            self.missionary.finish()
            self.missionary.create_new_after_finish()
            self.log.info('update missionary model successfully')
            send_missionary_pass(self.name)
            return True
        return False

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