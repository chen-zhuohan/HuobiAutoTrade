from backend.task.result import ResultType
from comm.instance import db
from models.base import UpdateBase


class Result(UpdateBase, db.Model):
    task = db.Column(db.CHAR(64), nullable=True)
    result = db.Column(db.VARCHAR(255), default='')
    pass_ = db.Column(db.BOOLEAN)

    @classmethod
    def create_by_result(cls, result):
        if result.type == ResultType.UNVALID:
            return
        cls.create(task=result.task_name,
                   result=result.short_str,
                   pass_=result.pass_)