from huobi_Python.huobi.model.order import Order

from comm.instance import db
from models.base import UpdateBase


class Trade(UpdateBase, db.Model):
    tradematch = db.Column(db.CHAR(64))
    amount = db.Column(db.Integer)
    price = db.Column(db.DECIMAL(10, 4))
    mission = db.Column(db.CHAR(64))
    type = db.Column(db.CHAR(64))

    def __str__(self):
        return '[trade: {}, amount: {}, mission: {}]'.format(self.tradematch, self.amount, self.mission)

    @classmethod
    def create_by_order(cls, order: Order, mission_name):
        if order.price < 0.0001:            # 卖出
            price = order.filled_cash_amount / order.filled_amount
        else:                               # 买入
            price = order.price

        return cls.create(amount=order.amount, mission=mission_name, tradematch=order.symbol,
                          price=price, type=order.order_type)