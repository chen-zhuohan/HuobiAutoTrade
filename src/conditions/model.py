import time

from common.instance import db
from common.model_help import UpdateModelBase


class Conditions(UpdateModelBase, db.Model):
    name = db.Column(db.VARCHAR(64), unique=True)
    expires = db.Column(db.INTEGER, nullable=True)
    valid = db.Column(db.BOOLEAN, default=True)

    @property
    def is_valid(self):
        if self.expires is None:
            return self.valid

        if time.time() < self.expires:
            return True
        else:
            return False