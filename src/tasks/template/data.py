from datas.interface import get_ma20, get_LB, get_UB, get_vol_vol3, get_present_period
from tasks.template.base import TaskTemplateBase


########################################################################################################################
# MA20
########################################################################################################################
class OpenBetweenMa20_10Percent(TaskTemplateBase):
    RULE = '开盘价在ma20上下10%的闭区间内'
    MSG_FORMAT = 'ma20为 {} 上下浮动10%的区间是 {} - {} ，开盘价是 {}'

    def try_pass(self, symbol, period) -> bool:
        ma20 = get_ma20(symbol=symbol, period=period)
        open_price = get_present_period(symbol=symbol, period=period).open
        open_min = ma20 * 0.90
        open_max = ma20 * 1.10

        self.msg_args = (ma20, open_min, open_max, open_price)
        if open_min <= open_price <= open_max:
            return True
        return False


class Now_LT_Ma20(TaskTemplateBase):
    RULE = '现价应该低于ma20'
    MSG_FORMAT = '现价: {} < ma20: {}'

    def try_pass(self, symbol, period) -> bool:
        ma20 = get_ma20(symbol=symbol, period=period)
        now_price = get_present_period(symbol=symbol).close

        self.msg_args = (now_price, ma20)
        if now_price < ma20:
            return True
        return False


########################################################################################################################
# VOL
########################################################################################################################
class Vol_GT_Vol3(TaskTemplateBase):
    RULE = '上一周期交易量大于前三周期交易量'
    MSG_FORMAT = '上一周期的交易总量{} > 上三周期的交易均值 {}'

    def try_pass(self, symbol, period) -> bool:
        vol, vol3 = get_vol_vol3(symbol=symbol, period=period)

        self.msg_args = (vol, vol3)
        if vol > vol3:
            return True
        return False


class Vol_LT_Vol3(TaskTemplateBase):
    RULE = '上一周期交易量小于前三周期交易量'
    MSG_FORMAT = '上一周期的交易总量{} < 上三周期的交易均值 {}'

    def try_pass(self, symbol, period) -> bool:
        vol, vol3 = get_vol_vol3(symbol=symbol, period=period)

        self.msg_args = (vol, vol3)
        if vol < vol3:
            return True
        return False


########################################################################################################################
# LB
########################################################################################################################
class Now_LT_LB(TaskTemplateBase):
    RULE = '现价应该低于布林下轨'
    MSG_FORMAT = '现价 {} < 布林下轨： {}'

    def try_pass(self, symbol, period) -> bool:
        now = get_present_period(symbol=symbol).close
        lb = get_LB(symbol=symbol, period=period)

        self.msg_args = (now, lb)
        if now < lb:
            return True
        return False


########################################################################################################################
# UB
########################################################################################################################
class Now_GT_UB(TaskTemplateBase):
    RULE = '现价应该高于布林上轨'
    MSG_FORMAT = '现价 {} > 布林上轨： {}'

    def try_pass(self, symbol, period) -> bool:
        now = get_present_period(symbol=symbol).close
        ub = get_UB(symbol=symbol, period=period)

        self.msg_args = (now, ub)
        if now > ub:
            return True
        return False


########################################################################################################################
# Other
########################################################################################################################
class Now_LT_Open(TaskTemplateBase):
    RULE = '现价应该低于这一周期开盘价'
    MSG_FORMAT = '现价 {} < 这一周期开盘价： {}'

    def try_pass(self, symbol, period) -> bool:
        kline = get_present_period(symbol=symbol, period=period)

        self.msg_args = (kline.close, kline.open)
        if kline.close < kline.open:
            return True
        return False