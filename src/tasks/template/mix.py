from datetime import datetime, timedelta

from common.utils import Logger
from conditions.interface import get_or_create_condition, get_condition_by_name
from datas.interface import get_present_period, get_LB, get_vol_vol3, get_UB
from tasks.template.trade import TradeTask
from trade.interface import Trade
from trade.interface import market_buy, market_sell

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


class ShortFirstStepV2(TradeTask):
    RULE = '现价应该低于布林下轨 && 第二次现价应该低于布林下轨 && 上一周期交易量大于前三周期交易量 && 市场买入'
    MSG_FORMAT = '现价 {} < 布林下轨： {} && 是否是第二次 {} && 上一周期的交易总量{} > 上三周期的交易均值 {} && 买入比例为: {}，货币对为: {}, 订单号为: {}'

    def try_pass(self, symbol, period, amount: int) -> bool:
        now = get_present_period(symbol=symbol).close
        lb = get_LB(symbol=symbol, period=period)

        if now >= lb:
            self.msg_args = (now, lb, None, None, None, None, None, None)
            return False
        ###############################################
        self.create_condition()
        if not self.is_second_pass():
            self.msg_args = (now, lb, False, None, None, None, None, None)
            return False

        ###############################################
        vol, vol3 = get_vol_vol3(symbol=symbol, period=period)

        # self.msg_args = (vol, vol3)
        if vol <= vol3:
            self.msg_args = (now, lb, True, vol, vol3, None, None, None)
            return False
        ###############################################
        try:
            order_id = market_buy(amount=amount, symbol=symbol)
            self.order_id = order_id
            self.msg_args = (now, lb, True, vol, vol3, amount, symbol, order_id)
            logger_buy.info('buy successfully, info: {}'.format(self.MSG_FORMAT.format(*self.msg_args)))
            return True
        except Exception as e:
            logger_buy.error('somethings wrong, detail: {}'.format(e.args))
            self.msg_args = (now, lb, True, vol, vol3, None, None, None)
            return False

    def create_condition(self):
        t = datetime.now()
        condition_name = f'lt lb at {t.strftime("%Y-%m-%d %H")}'
        condition = get_or_create_condition(condition_name)
        return condition

    def is_second_pass(self):
        t = datetime.now() - timedelta(hours=1)
        condition_name = f'lt lb at {t.strftime("%Y-%m-%d %H")}'
        condition_func = get_condition_by_name(condition_name)
        return condition_func()


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


class ShortStopLose(TradeTask):
    RULE = '买入价格和现价的差值占这个小时开盘价的3% && 市场卖出'
    MSG_FORMAT = '买入价格 {}， 现价 {}， 差价 {}， 这个小时开盘价 {}, 比值 {}% && 卖出比例为: {}，货币对为: {}, 订单号为: {}'

    def try_pass(self, mission_id: int, amount: int, symbol: str) -> bool:
        last_trade = Trade.get_last(mission_id=mission_id)
        if last_trade is None or last_trade.type != 'buy-market':
            logger_buy.info(f'last trade: {last_trade}, return here')
            self.msg_arg = (0, 0, 0, 0, 0, 0, 0, 0)
            self.need_record = False
            return False

        buy_price = float(last_trade.price)
        kline = get_present_period(symbol=last_trade.symbol, period='60min')
        now_price = kline.close
        last_hour_price = kline.open
        diff = buy_price - now_price
        p = diff / last_hour_price
        self.msg_args = (buy_price, now_price, diff, last_hour_price, p * 100, 0, 0, 0)
        if not (diff > 0 and p > 0.03):
            return False
        else:
            condition = get_or_create_condition('%stop lose%')
            if not condition.valid:
                condition.valid = True
                condition.save()

        try:
            order_id = market_sell(amount=amount, symbol=symbol)
            self.order_id = order_id
            self.msg_args = (buy_price, now_price, diff, last_hour_price, p * 100, amount, symbol, order_id)
            logger_buy.info('buy successfully, info: {}'.format(self.MSG_FORMAT.format(*self.msg_args)))
            return True
        except Exception as e:
            logger_buy.error('somethings wrong, detail: {}'.format(e.args))
            return False
