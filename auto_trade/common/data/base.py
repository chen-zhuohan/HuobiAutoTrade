from datetime import datetime, timedelta
import pytz
import requests
import time

from configs import HUOBI_URL
from common.email_helper import send_error
from common.utils import Logger


class Data:
    VALID_TIME = timedelta(hours=1)     # must to covered
    log = Logger('DATA BASE')

    def __init__(self, *args, **kwargs):
        self.log.clue = self.__class__.__name__
        self._data = None
        self.update_time = datetime.fromtimestamp(0)

    def __call__(self, *args, **kwargs):
        self.log.info('be called, is valid: {}'.format(self.has_valid))
        if not self.has_valid:
            self.update()
        self.log.info('data is {}'.format(self._data))
        return self._data

    def update(self):
        """ 更新数据 并做错误检查和重试 更新之后的数据在self._data"""
        ec = None
        for i in range(5):
            # self.update_data()
            # return
            try:
                self.log.info('try to update data')
                self.update_data()
                self.log.info('update data successfully')
                return
            except Exception as e:
                ec = e
                self.log.warning('update data fail, exception detail: {}, {}'.format(e, e.args))
                time.sleep(0.1)
        if ec:
            self.log.error('!!!update data tolly fail!!!, exception detail: {}, {}'.format(ec, ec.args))
            send_error(ec, extra='数据更新持续失败！')

    def update_data(self):
        """ 更新数据和时间 """
        self._data = self.get_data()
        self.update_time = datetime.now(tz=pytz.timezone('Asia/Shanghai'))

    @property
    def has_valid(self):
        if getattr(self, '_data', None):
            if datetime.now(tz=pytz.timezone('Asia/Shanghai')) - self.update_time < self.VALID_TIME:
                return True
        return False

    def get_data(self):
        # return data
        raise Exception('the func must be covered')


def base_query(symbol, period, size):
    params = dict(symbol=symbol, period=period, size=size)
    response = requests.get('https://' + HUOBI_URL + '/market/history/kline', params=params)
    data = response.json()['data']
    data.sort(key=lambda i: i['id'], reverse=True)
    return data


class BaseSymbolData(Data):
    def __init__(self, symbol):
        self.SYMBOL = symbol
        super().__init__()


class BaseQueryData(BaseSymbolData):
    SIZE = 0
    PERIOD = None

    def get_data(self):
        return base_query(symbol=self.SYMBOL, period=self.PERIOD, size=self.SIZE)


class BaseCalculateData(BaseSymbolData):
    def __init__(self, data_source, symbol):
        self.data_source = data_source
        super().__init__(symbol)