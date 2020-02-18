from huobi_Python.huobi.exception.huobiapiexception import HuobiApiException
from huobi_Python.huobi.requstclient import RequestClient
from huobi_Python.huobi.subscriptionclient import SubscriptionClient
from huobi_Python.huobi.model.constant import OrderType, AccountType, OrderSide, OrderState, CandlestickInterval
# Access Key
# 0883da63-2d9e92fa-c5535298-rbr45t6yr4
# Secret Key
# 8a338946-794b71c9-19c1aab3-04b5a
AccessKey = '0883da63-2d9e92fa-c5535298-rbr45t6yr4'
SecretKey = '8a338946-794b71c9-19c1aab3-04b5a'
url = 'api.huobi.pro'
# url = 'api-aws.huobi.pro'

request_client = RequestClient(api_key=AccessKey, secret_key=SecretKey, url='https://' + url)
subscription_client = SubscriptionClient(api_key=AccessKey, secret_key=SecretKey, url='wss://' + url)

# 获取isot的最好的出价和交易请求，在控制台上显示出交易的价格和数量
best_quote = request_client.get_best_quote("isot")
print(best_quote.ask_price)
print(best_quote.ask_amount)

# 订阅一只股票的数据，并定义一个函数去处理它
def callback(trade_event: 'TradeEvent'):
    print(trade_event.symbol)
    for trade in trade_event.trade_list:
        print(trade.price)

subscription_client.subscribe_trade_event("btcusdt", callback)

# 错误处理
# 对于请求客户端
try:
    best_quote = request_client.get_best_quote("abcdefg")
    print(best_quote.ask_price)
    print(best_quote.ask_amount)
except HuobiApiException as e:
    print(e.error_code)
    print(e.error_message)

# 对于订阅客户端
def callback(trade_event: 'TradeEvent'):
    print(trade_event.symbol)
    for trade in trade_event.trade_list:
        print(trade.price)

def error_handler(e: 'HuobiApiException'):
    print(e.error_code)
    print(e.error_message)

subscription_client.subscribe_trade_event("abcdefg", callback, error_handler)

# 提现
id = request_client.withdraw(address="xxxxxx", amount=2, currency="usdt", fee=1, chain="yyy", address_tag="zzz")
print(id)   # 提现交易的id

# 取消提现
request_client.cancel_withdraw("btc", id)

# 提现历史
withdraw_list = request_client.get_withdraw_history("btc", id, 10)
print(withdraw_list[0].amount)

# 存款历史
deposit_list = request_client.get_deposit_history("btc", id, 10)
print(deposit_list[0].amount)

# 创建订单
order_id = request_client.create_order("btcusdt", AccountType.SPOT, OrderType.BUY_LIMIT, 1.0, 1.0)
print(id)

# 取消订单
request_client.cancel_order("btcusdt", order_id)

# 取消未结订单
result = request_client.cancel_open_orders("btcusdt", AccountType.SPOT, OrderSide.SELL, 10)
print(result.success_count)

# 获取订单信息
order = request_client.get_order("symbol", id)
print(order.price)

# 历史订单
order_list = request_client.get_historical_orders("symbol", OrderState.SUBMITTED)
print(order_list[0].price)

# 订阅K线数据
def callback(candlestick_event: 'CandlestickEvent'):
    print(candlestick_event.data.high)
""" 这是订阅每分钟的，可以订阅别的时间段 """
subscription_client.subscribe_candlestick_event("btcusdt", CandlestickInterval.MIN15, callback)

# 订阅新的交易
def callback(trade_event: 'TradeEvent'):
    print(trade_event.symbol)
    for trade in trade_event.trade_list:
        print(trade.price)

subscription_client.subscribe_trade_event("btcusdt", callback)

# 取消订阅
subscription_client.unsubscribe_all()