from huobi_Python.huobi.requstclient import RequestClient
from huobi_Python.huobi.model.constant import OrderType, AccountType

from comm.utils import one_more_try
from configs import AccessKey, SecretKey, url, TRADEMATCH

request_client = RequestClient(api_key=AccessKey, secret_key=SecretKey, url='https://' + url)


@one_more_try('查询账户余额出错', max=3)
def get_all_spot_balance(type_):
    result = request_client.get_account_balance()
    for account in result:
        if account.account_state == 'working' and account.account_type == 'spot':
            for balance in account.get_balance(type_):
                if balance.balance > 1 and balance.balance_type == 'trade':
                    return balance.balance


def handel_precision(n):
    p = 10**2
    return (n * p // 1) / p


@one_more_try('买入出错', max=2, important=True)
def market_buy(amount, symbol):
    # return 0
    amount = handel_precision(amount)
    order_id = request_client.create_order(symbol, AccountType.SPOT, OrderType.BUY_MARKET, amount=amount, price=None)
    return order_id


@one_more_try('卖出出错', max=2, important=True)
def market_sell(amount, symbol):
    # return 0
    amount = handel_precision(amount)
    order_id = request_client.create_order(symbol, AccountType.SPOT, OrderType.SELL_MARKET, amount=amount, price=None)
    return order_id


@one_more_try('查询历史订单出错！', max=5)
def get_order(symbol, order_id):
    return request_client.get_order(symbol, order_id)


if __name__ == '__main__':
    data = request_client.get_order(TRADEMATCH, 68320042418)
    print(data)