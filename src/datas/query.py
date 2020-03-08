import requests
from typing import List

from common.utils import one_more_try
from configs import MARKET_KLINE_URL


class Kline:
    def __init__(self, data: dict):
        self.time = data['id']
        self.amount = data['amount']
        self.count = data['count']
        self.open = data['open']
        self.close = data['close']
        self.low = data['low']
        self.high = data['high']
        self.vol = data['vol']


@one_more_try(message='request huobi kline data；请求火币数据')
def get_kline_data(symbol: str, period: str, size: int) -> List[Kline]:
    """
    发送查询，获得数据字典组成的列表。
    :param symbol:such as btcusdt, thetausdt
    :param period: 1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1week, 1mon, 1year
    :param size: [1, 200]
    :return:list, sorted by time, the newest at first
    [{
        "id": 1499184000,       时间（起始时间）
        "amount": 37593.0266,   交易总额
        "count": 0,             交易次数
        "open": 1935.2000,      开盘价
        "close": 1879.0000,     收盘价/现价
        "low": 1856.0000,
        "high": 1940.0000,
        "vol": 71031537.97866500
    }, {...}, ...
    ]
    """
    params = dict(symbol=symbol, period=period, size=size)
    response = requests.get(MARKET_KLINE_URL, params=params)
    data = response.json()['data']
    data.sort(key=lambda i: i['id'], reverse=True)
    return [Kline(d) for d in data]


def get_kline_data_exclude_now_period(symbol: str, period: str, size: int) -> List[Kline]:
    return get_kline_data(symbol, period, size + 1)[1:]


def get_kline_data_at_present(symbol: str, period: str = '1min') -> Kline:
    return get_kline_data(symbol, period, 1)[0]
