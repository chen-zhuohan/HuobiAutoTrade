from celery.app.task import Task
from huobi.model.constant import OrderType

from common.instance import celery
from common.utils import Logger
from trade.huobi_client import get_order, market_buy, market_sell, get_all_spot_balance
from trade.model import Trade


logger = Logger('trade interface')


@celery.task(bind=True, name='记录订单', max_retries=20, default_retry_delay=30)
def record_by_order_id(self: Task, order_id: int, mission_id: int, mission_name: str, missionary_id: int):
    try:
        if order_id == 0:           # for test
            return
        order = get_order('thetausdt', order_id)
        price = order.filled_cash_amount / order.filled_amount
        if price == 0 or price is None:
            raise ValueError('market buy, the price should not be 0 or None')
        # if order.order_type == OrderType.SELL_MARKET:            # 卖出
        #     price = order.filled_cash_amount / order.filled_amount
        # elif order.order_type == OrderType.BUY_MARKET:           # 买入
        #     if order.price == 0 or order.price is None:
        #         raise ValueError('market buy, the price should not be 0 or None')
        #     price = order.price
        # else:
        #     raise TypeError('unexpect order type')

        return Trade.create(amount=order.amount, symbol=order.symbol,
                            price=price, type=order.order_type,
                            mission_id=mission_id, mission_name=mission_name, missionary_id=missionary_id)
    except Exception as e:
        logger.warning('try to record trade fail, detail: {}, retry: {}'.format(e, self.request.retries))
        self.retry(exc=e)

# buy order print
# 2020-04-09 20:01:03+08:00
# Order Id : 79803178157
# Symbol : thetausdt
# Price : 0.0
# Amount : 384.0
# Create Time : 1586433663169
# Cancel Time : 0
# Finish Time : 1586433663314
# Order Type : buy-market
# Filled Amount : 4499.121779859484
# Filled Cash Amount : 384.0
# Filled Fees : 8.99824355971897
# Account Type : spot
# Order Source : api
# Order State : filled
# Stop Price : 0.0
# Operator :
# Next Time :
