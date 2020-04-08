# huobi:
AccessKey = 'mn8ikls4qg-f444bdb9-825a1319-69dc6'
# SecretKey = '54c7975a-453c4611-15711bf9-ba479'
SecretKey = '54c7975a-453c4611-15711bf'
# HUOBI_URL = 'api.huobi.de.com'    # 不用翻墙
HUOBI_URL = 'api.huobi.pro'
# HUOBI_URL = 'api-aws.huobi.pro'
# theta是你要买的，usdt是中间火币
BUY_CURRENCY = 'btc'
MIDDLE_CURRENCY = 'usdt'
TRADE_MATCH = BUY_CURRENCY + MIDDLE_CURRENCY


from huobi.model import OrderState, Account, Balance
from huobi.model.constant import OrderType, AccountType
from huobi.requstclient import RequestClient

# from configs import AccessKey, SecretKey, HUOBI_URL

request_client = RequestClient(api_key=AccessKey, secret_key=SecretKey, url='https://' + HUOBI_URL)


def handel_precision(n):
    p = 10**2
    return (n * p // 1) / p


def market_buy(amount: int, symbol: str) -> int:
    amount = handel_precision(amount)
    print(f'will buy {amount} {TRADE_MATCH}')
    order_id = request_client.create_order(symbol, AccountType.SPOT, OrderType.BUY_MARKET, amount=amount, price=None)
    return int(order_id)


def market_sell(amount: int, symbol: str) -> int:
    amount = handel_precision(amount)
    print(f'will sell {amount} {TRADE_MATCH}')
    order_id = request_client.create_order(symbol, AccountType.SPOT, OrderType.SELL_MARKET, amount=0.001, price=None)
    return int(order_id)


def get_account():
    account: Account = request_client.get_account_balance_by_account_type(AccountType.SPOT)
    for b in account.balances:
        if b.balance < 0.000000001:
            continue
        print('#'*30)
        print(b.currency)
        print(b.balance)
    print(account.get_balance('usdt'))
    print(account.get_balance('btc'))


if __name__ == '__main__':
    # market_buy(5, TRADE_MATCH)
    # market_sell(1, TRADE_MATCH)
    get_account()