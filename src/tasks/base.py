"""
每个任务有多样的先置条件，包括时间和上一个任务的完成。
每个任务自己只保证自己的执行时间，一个大的任务链条来保证执行顺序。
当一个任务执行成功，则保存到数据库一条记录。
在定时任务启动时，根据指定的任务名，从数据库读取最后一条记录
SELECT * FROM `user`  ORDER BY id DESC  LIMIT  1
"""
# from auto_trade.backend import Result, UnvalidResult
#
#
class TaskBase:
    RULE = None
    MSG = None

    def __init__(self):
        self.msg_arg = tuple()

    def pass_(self, force=False):
        if self.is_valid or force:
            if self.pass_condition():
                return Result.create_by_task(self, True)
            else:
                return Result.create_by_task(self, False)
        return UnvalidResult()

    @property
    def is_valid(self):
        return self.run_condition()

    def run_condition(self):
        raise Exception('must be covered')

    def pass_condition(self):
        raise Exception('must be covered')


class TaskEngine:
    def can_run(self) -> bool:
        pass

    def passed(self, mission_engine, index=-1) -> bool:
        pass

    # @property
    # def is_passed(self) -> Result:
    #     pass