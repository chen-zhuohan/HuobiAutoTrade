from tasks.engine import TaskEngine


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
    return CONSTANT_ID_TASK_MAP.get(id_)


def get_task_run_time_by_id(id_: int) -> str:
    return CONSTANT_ID_TASK_MAP.get(id_).run_time