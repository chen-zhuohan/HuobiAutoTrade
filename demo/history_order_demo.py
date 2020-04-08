from huobi.model import OrderState
from huobi.requstclient import RequestClient
from huobi.model.trade import Trade

from datetime import datetime
import pytz

from configs import AccessKey, SecretKey, HUOBI_URL
timezone = 'Asia/Shanghai'
TIMEZONE = pytz.timezone(timezone)
request_client = RequestClient(api_key=AccessKey, secret_key=SecretKey, url='https://' + HUOBI_URL)

symbol = 'btcusdt'
size = 10

trade_list = request_client.get_historical_trade(symbol, size)
#
for trade in trade_list:
    print('#' * 30)
    d = datetime.fromtimestamp(trade.timestamp//1000, tz=TIMEZONE)
    print(d)
    print(trade)
    print(type(trade))
    trade.print_object()

#
#
# print('#'*30)
# order_list = request_client.get_historical_orders(symbol, OrderState.SUBMITTED)
# for order in order_list:
#     order.print_object()


# order_list = request_client.get_order_recent_48hour(symbol)
# for order in order_list:
#     print('#'*30)
#     order.print_object()
