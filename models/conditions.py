from comm.instance import db
from models.base import UpdateBase


class CONDITION_TYPE:
    stop_lose = 1


class Conditions(UpdateBase, db.Model):
    type = db.Column(db.SMALLINT)
    valid = db.Column(db.BOOLEAN, default=True)