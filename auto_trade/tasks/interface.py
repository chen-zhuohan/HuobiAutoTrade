from tasks.base import TaskEngine


def get_task_by_id(id_) -> TaskEngine:
    if id_ == 0:
        return AlwaysTrue()
    if id_ == -1:
        return AlwaysFalse


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