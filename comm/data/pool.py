from comm.data.datas import BaseMatch

BTCtoUSDT = BaseMatch('btcusdt')
THETAtoUSDT = BaseMatch('thetausdt')


class DataPool:
    # 有多种数据，每种数据都应该有一个过期时间，有一个来源，有一个查询参数。
    # 除了原始数据外，还有计算之后的数据，比如周布林下轨，月布林下轨啥的。
    @classmethod
    def add(cls, data):
        setattr(cls, data.__name__, data())

    BTCtoUSDT = BTCtoUSDT
    THETAtoUSDT = THETAtoUSDT