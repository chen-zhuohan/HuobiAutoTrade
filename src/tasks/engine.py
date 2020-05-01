import importlib
import inspect

from common.utils import Logger
from tasks.result import Result
from tasks.template.base import TaskTemplateBase
from tasks.template.trade import TradeTask
from tasks.models.task import Task
from tasks.models.result_log import ResultLog
from conditions.interface import get_condition_by_name
from trade.interface import record_by_order_id


task_template_set = importlib.import_module('tasks.template.__init__')
task_template_dict = dict()

for name, obj in inspect.getmembers(task_template_set):
    print(name, obj)
    if inspect.isclass(obj) and issubclass(obj, TaskTemplateBase):
        task_template_dict[name] = obj


class TaskEngine:
    logger = Logger('Task engine')

    def __init__(self, task_id=None):
        if task_id is None:         # for test
            return

        task = Task.query.filter_by(id=task_id).first()
        self.task_id = None
        self.task_name = None
        self.kwargs = None
        self.run_time = None
        self.can_run_str = None
        self.task = None
        self.init_task(task)

        self.task_index = None
        self.mission_id = None
        self.mission_name = None
        self.missionary_id = None

    def __str__(self):
        return '[{}]'.format(self.task_name)

    def init_task(self, task):
        self.task_id = task.id
        self.task_name = task.name
        self.kwargs = task.kwargs
        self.run_time = task.run_time
        self.can_run_str = task.can_run
        self.task = task_template_dict[task.template_name]()
        self.logger.clue = self.task_name

    def get_info_from_mission(self, index: int = 0, mission_engine=None):
        # 0 is target
        self.task_index = index
        self.mission_id = mission_engine.mission_id
        self.mission_name = mission_engine.name
        self.missionary_id = mission_engine.missionary.id

    def can_run(self) -> bool:
        if not hasattr(self, '_can_run'):
            self._can_run = get_condition_by_name(self.can_run_str)
        return self._can_run()

    def try_pass(self) -> bool:
        self.logger.info('try to pass task')
        is_pass = self.task.try_pass(**self.kwargs)
        self.logger.info('task pass completed, result: {}'.format(is_pass))

        result = self.create_result_log(is_pass)

        if is_pass and issubclass(self.task.__class__, TradeTask):        # 记录交易结果
            order_id = self.task.order_id
            record_by_order_id.delay(order_id, self.mission_id, self.mission_name, self.missionary_id)
            self.logger.info('task is type of trade, save trade record has in async.order id: {}'.format(order_id))
            self.logger.info('task is type of trade, save trade record has in async.order id: {}'.format(order_id))
        return result

    def create_result_log(self, is_pass):
        result = Result.create_by_task_engine(self, is_pass)
        self.logger.info('create result by task engine successfully, result: {}'.format(result))
        if self.task.need_record:
            result_log = ResultLog.save_from_task_engine(self)
            self.logger.info('create result log by task engine successfully, result_log id: {}'.format(result_log.id))
            self.logger.info('task type: {}'.format(type(self.task)))

        return result
