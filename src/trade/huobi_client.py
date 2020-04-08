from huobi.requstclient import RequestClient
from huobi.model.constant import OrderType, AccountType
from huobi.model import OrderState, Account

from common.utils import one_more_try, Logger
from configs import AccessKey, SecretKey, HUOBI_URL, TRADE_MATCH, TESTING, NOTTRADE


huobi_logger = Logger('huobi')

huobi_logger.info(f'AccessKey: {AccessKey}')
huobi_logger.info(f'SecretKey: {SecretKey}')


def get_request_client():
    return RequestClient(api_key=AccessKey, secret_key=SecretKey, url=HUOBI_URL)


@one_more_try('查询账户余额', max=3)
def get_all_spot_balance(type_):
    request_client = get_request_client()
    huobi_logger.info(f'request_client.get_account_balance_by_account_type({AccountType.SPOT})')
    account: Account = request_client.get_account_balance_by_account_type(AccountType.SPOT)
    for balance in account.balances:
        if type_ == balance.currency and balance.balance > 0.000000001:
            return int(balance.balance)

    return 0


def handel_precision(n):
    """ 获得 usdt，处理精度 """
    balance = get_all_spot_balance('usdt')
    n = n / 100 * balance
    p = 10**2
    return (n * p // 1) / p


@one_more_try('买入', max=5, important=True)
def market_buy(amount: int, symbol: str) -> int:
    request_client = get_request_client()
    if NOTTRADE:
        return 0
    amount = handel_precision(amount)
    huobi_logger.info(f'request_client.create_order({symbol}, {AccountType.SPOT}, {OrderType.BUY_MARKET}, amount={amount}, price={None})')
    order_id = request_client.create_order(symbol, AccountType.SPOT, OrderType.BUY_MARKET, amount=amount, price=None)
    return int(order_id)


@one_more_try('卖出', max=2, important=True)
def market_sell(amount: int, symbol: str) -> int:
    request_client = get_request_client()
    if NOTTRADE:
        return 0
    amount = handel_precision(amount)
    huobi_logger.info(f'request_client.create_order({symbol}, {AccountType.SPOT}, {OrderType.SELL_MARKET}, amount={amount}, price={None})')
    order_id = request_client.create_order(symbol, AccountType.SPOT, OrderType.SELL_MARKET, amount=amount, price=None)
    return int(order_id)


@one_more_try('查询历史订单', max=5)
def get_order(symbol, order_id):
    request_client = get_request_client()
    return request_client.get_order(symbol, order_id)
