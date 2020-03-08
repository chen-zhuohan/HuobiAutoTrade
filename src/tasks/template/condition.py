from conditions.interface import Conditions
from datas.interface import get_present_period
from tasks.template.base import TaskTemplateBase
from trade.interface import Trade


class ConditionTask(TaskTemplateBase):
    def save_condition(self):
        raise Exception('must be cover')


class StopLose(ConditionTask):
    RULE = '买入价格和现价的差值占这个小时开盘价的3%'
    MSG_FORMAT = '买入价格 {}， 现价 {}， 差价 {}， 这个小时开盘价 {}, 比值 {}%'

    def try_pass(self, mission_id) -> bool:
        last_trade = Trade.get_last(mission_id=mission_id, type='buy-market')
        if last_trade is None:
            self.msg_arg = (0, 0, 0, 0, 0)
            return False

        buy_price = float(last_trade.price)
        kline = get_present_period(symbol=last_trade.symbol, period='60min')
        now_price = kline.close
        last_hour_price = kline.open
        diff = buy_price - now_price
        p = diff/last_hour_price
        self.msg_args = (buy_price, now_price, diff, last_hour_price, p*100)
        if diff > 0 and p > 0.03:
            # TODO: move to others
            Conditions.create(name='stop lose', valid=True)
            return True

        return False