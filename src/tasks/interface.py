from tasks.base import TaskEngine


class AlwaysTrue(TaskEngine):
    def can_run(self, *args, **kwargs):
        return True

    def passed(self, *args, **kwargs):
        return True


class AlwaysFalse(TaskEngine):
    def can_run(self, *args, **kwargs):
        return False

    def passed(self, *args, **kwargs):
        return False


class NotPassed(TaskEngine):
    def can_run(self, *args, **kwargs):
        return True

    def passed(self, *args, **kwargs):
        return False


CONSTANT_ID_TASK_MAP = {
    0: AlwaysTrue(),
    -1: AlwaysFalse(),
    -2: NotPassed(),
}


def get_task_by_id(id_) -> TaskEngine:
    return CONSTANT_ID_TASK_MAP.get(id_)


