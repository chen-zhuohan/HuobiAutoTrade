import importlib
import inspect

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
    if inspect.isclass(obj) and issubclass(obj, TaskTemplateBase):
        task_template_dict[name] = obj


class TaskEngine:
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
        return '{[{name}, run_time: {run_time}]}'.format(name=self.__name__, run_time=self.run_time)

    def init_task(self, task):
        self.task_id = task.id
        self.task_name = task.name
        self.kwargs = task.kwargs
        self.run_time = task.run_time
        self.can_run_str = task.can_run
        self.task = task_template_dict[task.template_name]()

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
        is_pass = self.task.try_pass(**self.kwargs)
        result = Result.create_by_task_engine(self, is_pass)
        ResultLog.save_from_task_engine(self)

        if is_pass and issubclass(self.task, TradeTask):        # 记录交易结果
            order_id = self.task.order_id
            record_by_order_id.delay(order_id, self.mission_id, self.mission_name, self.missionary_id)
        
        return result