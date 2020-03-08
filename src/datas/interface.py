from datas.calculate import calculate_UB, calculate_LB, calculate_vol_vol3, calculate_ma
from datas.query import get_kline_data_exclude_now_period, get_kline_data_at_present, Kline


def get_ma20(symbol: str, period: str) -> int:
    data = get_kline_data_exclude_now_period(symbol=symbol, period=period, size=20)
    return calculate_ma(data)


def get_LB(symbol: str, period: str) -> int:
    data = get_kline_data_exclude_now_period(symbol=symbol, period=period, size=20)
    return calculate_LB(data)


def get_UB(symbol: str, period: str) -> int:
    data = get_kline_data_exclude_now_period(symbol=symbol, period=period, size=20)
    return calculate_UB(data)


def get_vol_vol3(symbol: str, period: str) -> int:
    data = get_kline_data_exclude_now_period(symbol=symbol, period=period, size=3)
    return calculate_vol_vol3(data)


def get_present_period(symbol: str, period: str = '1min') -> Kline:
    return get_kline_data_at_present(symbol=symbol, period=period)