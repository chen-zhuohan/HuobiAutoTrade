from datetime import timedelta

from comm.data.calculate import calculate_DN, calculate_ma20, calculate_vol_vol3, calculate_UN
from comm.data.base import BaseCalculateData, BaseQueryData


class Weeks21(BaseQueryData):
    SIZE = 21
    PERIOD = '1week'
    VALID_TIME = timedelta(weeks=1)


class Days21(BaseQueryData):
    SIZE = 21
    PERIOD = '1day'
    VALID_TIME = timedelta(days=1)


class Hours21(BaseQueryData):
    SIZE = 21
    PERIOD = '60min'
    VALID_TIME = timedelta(hours=1)


class WeekNow(BaseQueryData):
    SIZE = 1
    PERIOD = '1week'
    VALID_TIME = timedelta(seconds=1)


class OpenMA20Weeks(BaseCalculateData):
    """前20周的收盘价的平均值"""
    VALID_TIME = timedelta(weeks=1)

    def get_data(self):
        data = self.data_source.Weeks21()
        return calculate_ma20(data[1:])


class OpenMA20Days(BaseCalculateData):
    """前20天的收盘价的平均值"""
    VALID_TIME = timedelta(days=1)

    def get_data(self):
        data = self.data_source.Days21()
        return calculate_ma20(data[1:])


class NowPrice(BaseCalculateData):
    VALID_TIME = timedelta(seconds=1)

    def get_data(self):
        return self.data_source.WeekNow()[0]['close']


class VolaVol3Week(BaseCalculateData):
    """ 获得上周的交易量和 & 前三周交易量的均值"""
    VALID_TIME = timedelta(weeks=1)

    def get_data(self):
        data = self.data_source.Weeks21()
        return calculate_vol_vol3(data[1:4])


class WeekDN(BaseCalculateData):
    VALID_TIME = timedelta(weeks=1)

    def get_data(self):
        data = self.data_source.Weeks21()
        return calculate_DN(data[1:])


class HourDN(BaseCalculateData):
    VALID_TIME = timedelta(hours=1)

    def get_data(self):
        data = self.data_source.Hours21()
        return calculate_DN(data[1:])


class HourUN(BaseCalculateData):
    VALID_TIME = timedelta(hours=1)

    def get_data(self):
        data = self.data_source.Hours21()
        return calculate_UN(data[1:])


class VolaVol3Hour(BaseCalculateData):
    """ 获得上小时的交易量和 & 前三周交易量的均值"""
    VALID_TIME = timedelta(hours=1)

    def get_data(self):
        data = self.data_source.Hours21()
        return calculate_vol_vol3(data[1:4])


class BaseMatch:
    def __init__(self, symbol):
        self.Weeks21 = Weeks21(symbol)
        self.Days21 = Days21(symbol)
        self.Hours21 = Hours21(symbol)
        self.WeekNow = WeekNow(symbol)

        self.NowPrice = NowPrice(self, symbol)
        self.OpenMA20Weeks = OpenMA20Weeks(self, symbol)
        self.OpenMA20Days = OpenMA20Days(self, symbol)
        self.VolaVol3Week = VolaVol3Week(self, symbol)
        self.VolaVol3Hour = VolaVol3Hour(self, symbol)
        self.WeekDN = WeekDN(self, symbol)
        self.HourDN = HourDN(self, symbol)
        self.HourUN = HourUN(self, symbol)