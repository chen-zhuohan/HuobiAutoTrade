from comm.instance import db
from models.base import UpdateBase


class TaskPass(UpdateBase, db.Model):
    task_id = db.Column(db.SMALLINT)
    task = db.Column(db.CHAR(64), nullable=True)
    mission_start = db.Column(db.VARCHAR(64))
    mission = db.Column(db.CHAR(64))
    is_end = db.Column(db.BOOLEAN, default=False)
    result = db.Column(db.VARCHAR(255),default='')