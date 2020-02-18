class ResultType:
    NORMAL = 1
    UNVALID = 2
    DEFAULT = 3


class Result:
    def __init__(self, msg: str, pass_: bool, rule: str, task_name: str):
        self.type_ = ResultType.NORMAL
        self.task_name = task_name
        self.msg = msg
        self.pass_ = pass_
        self.rule = rule

    def __bool__(self):
        return self.pass_

    def __str__(self):
        result = '\n'.join((self.rule, self.msg, '<' + '='*50 + '>'))
        return result

    @classmethod
    def create_by_task(cls, task, pass_):
        if pass_:
            msg = 'PASS ' + task.MSG.format(*task.msg_arg)
        else:
            msg = 'FAIL ' + task.MSG.format(*task.msg_arg)

        return cls(msg, pass_, task.RULE, task.__class__.__name__)

    @property
    def short_str(self):
        return self.msg


class DefaultResult(Result):
    def __init__(self, task_name=''):
        self.type_ = ResultType.DEFAULT
        self.task_name = str(task_name)
        self.msg = '嘤嘤嘤'
        self.pass_ = False
        self.rule = 'No Rule'


class UnvalidResult(Result):
    def __init__(self, task_name=''):
        self.type_ = ResultType.UNVALID
        self.task_name = str(task_name)
        self.msg = '嘤嘤嘤'
        self.pass_ = False
        self.rule = 'No Rule'