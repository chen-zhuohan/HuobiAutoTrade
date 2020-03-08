from common.instance import db
from common.model_help import UpdateModelBase


class Trade(UpdateModelBase, db.Model):
    symbol = db.Column(db.CHAR(64))
    amount = db.Column(db.Integer)
    price = db.Column(db.DECIMAL(10, 4))

    mission_id = db.Column(db.INTEGER)
    mission_name = db.Column(db.CHAR(64))
    missionary_id = db.Column(db.INTEGER)
    type = db.Column(db.CHAR(64))

    def __str__(self):
        return '[trade: {}, amount: {}, mission: {}]'.format(self.symbol, self.amount, self.mission)