from common.instance import db
from common.model_help import UpdateModelBase


class Trade(UpdateModelBase, db.Model):
    symbol = db.Column(db.VARCHAR(64))
    amount = db.Column(db.Integer)
    price = db.Column(db.DECIMAL(10, 4))

    mission_id = db.Column(db.INTEGER)
    mission_name = db.Column(db.VARCHAR(64))
    missionary_id = db.Column(db.INTEGER)
    type = db.Column(db.VARCHAR(64))

    def __str__(self):
        return '[mission:{} {} {}, ]'.format(self.mission_name, self.type, self.symbol)
