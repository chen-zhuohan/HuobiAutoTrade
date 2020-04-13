from trade.interface import market_buy, market_sell
from common.utils import Logger
from tasks.template.base import TaskTemplateBase

logger_buy = Logger('market buy task')
logger_sell = Logger('market sell task')


class TradeTask(TaskTemplateBase):
    def __init__(self, *args, **kwargs):
        self.order_id = None
        super().__init__(*args, **kwargs)


class MARKET_BUY(TradeTask):
    RULE = '市场买入'
    MSG_FORMAT = '买入比例为: {}，货币对为: {}, 订单号为: {}'

    def try_pass(self, amount: int, symbol: str) -> bool:
        try:
            order_id = market_buy(amount=amount, symbol=symbol)
            self.order_id = order_id
            self.msg_args = (amount, symbol, order_id)
            logger_buy.info('buy successfully, info: {}'.format(self.MSG_FORMAT.format(*self.msg_args)))
            return True
        except Exception as e:
            logger_buy.error('somethings wrong, detail: {}'.format(e.args))
            return False


class MARKET_SELL(TradeTask):
    RULE = '市场卖出'
    MSG_FORMAT = '卖出比例为: {}，货币对为: {}, 订单号为: {}'

    def try_pass(self, amount: int, symbol: str) -> bool:
        try:
            order_id = market_sell(amount=amount, symbol=symbol)
            self.order_id = order_id
            self.msg_args = (amount, symbol, order_id)
            logger_buy.info('buy successfully, info: {}'.format(self.MSG_FORMAT.format(*self.msg_args)))
            return True
        except Exception as e:
            logger_buy.error('somethings wrong, detail: {}'.format(e.args))
            return False
