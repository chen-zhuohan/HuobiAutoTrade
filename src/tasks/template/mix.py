from datas.interface import get_present_period, get_LB, get_vol_vol3, get_UB
from tasks.template.trade import TradeTask
from trade.interface import market_buy, market_sell
from common.utils import Logger
from tasks.template.base import TaskTemplateBase

logger_buy = Logger('market buy task')
logger_sell = Logger('market sell task')


class ShortFirstStep(TradeTask):
    RULE = '现价应该低于布林下轨 && 上一周期交易量大于前三周期交易量 && 市场买入'
    MSG_FORMAT = '现价 {} < 布林下轨： {} && 上一周期的交易总量{} > 上三周期的交易均值 {} && 买入比例为: {}，货币对为: {}, 订单号为: {}'

    def try_pass(self, symbol, period, amount: int) -> bool:
        now = get_present_period(symbol=symbol).close
        lb = get_LB(symbol=symbol, period=period)

        if now >= lb:
            self.msg_args = (now, lb, None, None, None, None, None)
            return False
        ###############################################
        vol, vol3 = get_vol_vol3(symbol=symbol, period=period)

        # self.msg_args = (vol, vol3)
        if vol <= vol3:
            self.msg_args = (now, lb, vol, vol3, None, None, None)
            return False
        ###############################################
        try:
            order_id = market_buy(amount=amount, symbol=symbol)
            self.order_id = order_id
            self.msg_args = (now, lb, vol, vol3, amount, symbol, order_id)
            logger_buy.info('buy successfully, info: {}'.format(self.MSG_FORMAT.format(*self.msg_args)))
            return True
        except Exception as e:
            logger_buy.error('somethings wrong, detail: {}'.format(e.args))
            self.msg_args = (now, lb, vol, vol3, None, None, None)
            return False


class ShortSecondStep(TradeTask):
    RULE = '现价应该高于布林上轨 && 市场卖出'
    MSG_FORMAT = '现价 {} > 布林上轨： {} && 卖出比例为: {}，货币对为: {}, 订单号为: {}'

    def try_pass(self, symbol, period, amount) -> bool:
        now = get_present_period(symbol=symbol).close
        ub = get_UB(symbol=symbol, period=period)

        self.msg_args = (now, ub, None, None, None)
        if now <= ub:
            return False
        #############################################################################
        try:
            order_id = market_sell(amount=amount, symbol=symbol)
            self.order_id = order_id
            self.msg_args = (now, ub, amount, symbol, order_id)
            logger_buy.info('buy successfully, info: {}'.format(self.MSG_FORMAT.format(*self.msg_args)))
            return True
        except Exception as e:
            logger_buy.error('somethings wrong, detail: {}'.format(e.args))
            return False
