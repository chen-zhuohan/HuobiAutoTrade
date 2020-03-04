import requests

from common.huobi_client import request_client
from common.utils import one_more_try
from configs import MARKET_KLINE_URL


@one_more_try(message='request huobi kline data；请求火币数据')
def get_kline_data(symbol: str, period: str, size: int) -> list:
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
    return data


def get_kline_data_exclude_now_period(symbol: str, period: str, size: int) -> list:
    size += 1
    return get_kline_data(symbol, period, size)[1:]


def get_kline_data_at_present(symbol: str) -> dict:
    return get_kline_data(symbol, '1min', 1)[0]