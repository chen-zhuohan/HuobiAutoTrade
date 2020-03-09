from common.utils import Logger

class ResultType:
    NORMAL = 1
    UNVALID = 2
    DEFAULT = 3


class Result:
    logger = Logger('result')

    def __init__(self, msg: str, pass_: bool, rule: str, index: int, task_id: int,
                 task_name: str, mission_name: str):

        self.index = index
        self.task_id = task_id
        self.task_name = task_name
        self.mission_name = mission_name

        self.pass_ = pass_
        self.msg = msg
        self.rule = rule

    def __bool__(self):
        return self.pass_

    def __str__(self):
        result = '\n'.join((self.rule, self.msg, '<' + '='*50 + '>'))
        return result

    @classmethod
    def create_by_task_engine(cls, task_engine, pass_):
        cls.logger.info('try to create by task engine')
        task = task_engine.task
        if pass_:
            msg = 'PASS ' + task.msg
        else:
            msg = 'FAIL ' + task.msg
        return cls(msg, pass_, task.RULE, task_engine.task_index, task_engine.task_id,
                   task_engine.task_name, task_engine.mission_name)

    @property
    def short_str(self):
        return self.msg
