from tasks.engine import TaskEngine
from tasks.models.task import Task


class AlwaysTrue(TaskEngine):
    run_time = '1min'

    def can_run(self, *args, **kwargs):
        return True

    def try_pass(self, *args, **kwargs):
        return True


class AlwaysFalse(TaskEngine):
    run_time = '1min'

    def can_run(self, *args, **kwargs):
        return False

    def try_pass(self, *args, **kwargs):
        return False


class NotPassed(TaskEngine):
    run_time = '1min'

    def can_run(self, *args, **kwargs):
        return True

    def try_pass(self, *args, **kwargs):
        return False


class FiftyMinTask(TaskEngine):
    run_time = '15min'

    def can_run(self, *args, **kwargs):
        return True

    def try_pass(self, *args, **kwargs):
        return True


CONSTANT_ID_TASK_MAP = {
    0: AlwaysTrue(),
    -1: AlwaysFalse(),
    -2: NotPassed(),
    -3: FiftyMinTask()
}


def get_task_by_id(id_) -> TaskEngine:
    if id_ in CONSTANT_ID_TASK_MAP:
        return CONSTANT_ID_TASK_MAP.get(id_)
    else:
        return TaskEngine(task_id=id_)


def get_task_run_time_by_id(id_: int) -> str:
    if id_ in CONSTANT_ID_TASK_MAP:
        return CONSTANT_ID_TASK_MAP.get(id_).run_time
    else:
        return Task.query.filter_by(id=id_).with_entities('id', 'run_time').first()[1]