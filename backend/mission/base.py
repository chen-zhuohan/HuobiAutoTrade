import time

from backend.task.result import DefaultResult
from models.trade import Trade
from models.task_pass import TaskPass
from models.conditions import Conditions
from models.result import Result
from comm.email_helper import send_task_pass, send_trade
from comm.utils import Logger
from comm.time_helper import now_format_time


class MissionBase:
    """
    连接各个task，执行买入，独写数据库的操作
    """
    TASKLINE = list()
    NAME = None
    log = Logger('MISSION')

    def __init__(self):
        self.start_time = None
        self.log.clue = self.NAME
        self.last_result = DefaultResult(self.NAME)

    def pass_(self, force=False):
        next_task = self.get_last_finished_task_id() + 1
        self.log.info('next task id is {}'.format(next_task))
        for task in self.TASKLINE[next_task:]:
            result = task().pass_(force=False)
            Result.create_by_result(result)
            self.last_result = result
            if not result:          # 如果有一个不成功，那就玩完了
                self.log.info('{} not pass, detail: {}'.format(task, result))
                return False

            self.log.info('{} pass, bool: {}, detail: {}'.format(task, result.__bool__, result))
            self.save_pass_record(task)
            send_task_pass(result)
        return True

    def show_info(self):
        result = []
        for task in self.TASKLINE:
            result.append(task().pass_(True))
        return result

    def get_last_finished_task_id(self) -> int:
        # 如果一条都找不到，或找到的已经is end=True，创建一条-1，否则返回正常值
        start = time.time()
        self.log.info('try to get_last_finished_task_id')
        result = TaskPass.get_last(mission=self.NAME)
        if result is None or result.is_end:
            self.log.info('first run, result: {}'.format(result))
            self.create_first_record()
            return -1

        self.start_time = result.mission_start
        self.log.info('get_last_finished_task_id cost {}'.format(time.time() - start))
        return result.task_id

    def create_first_record(self):
        self.start_time = now_format_time()
        tp = TaskPass(mission_start=self.start_time, mission=self.NAME, task_id=-1)
        tp.save()
        self.log.info('create first recode, task pass: {}'.format(tp))

    def save_pass_record(self, task):
        if getattr(self, 'start_time', False):
            mp = TaskPass(task=task.__class__.__name__,
                          mission_start=self.start_time,
                          mission=self.NAME,
                          task_id=self.TASKLINE.index(task))
            if mp.task_id == len(self.TASKLINE) - 1:
                mp.is_end = True
            mp.save()
        else:
            self.create_first_record()

    @classmethod
    def run(cls):
        if cls.can_run:
            m = cls()
            m.do_run()
            return m
        else:
            raise Exception('cant run')

    @property
    def can_run(self):
        return not Conditions.query.filter_by(valid=True).exists()

    def do_run(self):
        raise Exception('must be covered')


class MissionForBuy(MissionBase):
    Trade = None

    def __init__(self, *args, **kwargs):
        self.check_pre_init()
        super().__init__(*args, **kwargs)

    def check_pre_init(self):
        if self.Trade is None:
            raise Exception('Trade should not be None')

    def do_run(self):
        self.log.info('mission.start')
        start = time.time()
        if self.pass_():
            order = self.Trade(self.NAME).buy()
            trade = Trade.create_by_order(order, self.NAME)
            send_trade('成功买入!', trade)
        self.log.info('MissionForBuy.run cost {}'.format(time.time() - start))


class MissionForSell(MissionBase):
    Trade = None

    def __init__(self, *args, **kwargs):
        self.check_pre_init()
        super().__init__(*args, **kwargs)

    def check_pre_init(self):
        if self.Trade is None:
            raise Exception('Trade should not be None')

    def do_run(self):
        if self.pass_():
            order = self.Trade(self.NAME).sell()
            trade = Trade.create_by_order(order, self.NAME)
            send_trade('成功卖出!', trade)