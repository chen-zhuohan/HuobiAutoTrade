from common.instance import db
from common.model_help import UpdateModelBase


class ResultLog(UpdateModelBase):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.VARCHAR(255))
    task_id = db.Column(db.SMALLINT)
    task_index = db.Column(db.SMALLINT)
    mission_id = db.Column(db.Integer)
    missionary_id = db.Column(db.Integer)

    msg = db.Column(db.VARCHAR(255))

    @classmethod
    def save_from_task_engine(cls, task_engine):
        result = cls(task_name=task_engine.task_name,
                     task_id=task_engine.task_id,
                     task_index=task_engine.task_index,
                     mission_id=task_engine.mission_id,
                     missionary_id=task_engine.missionary_id,
                     msg=task_engine.task.msg)
        result.save()
        return result