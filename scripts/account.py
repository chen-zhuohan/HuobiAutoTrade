from argparse import ArgumentParser, _SubParsersAction


def register(subparsers: _SubParsersAction):
    parse = subparsers.add_parser('account')
    parse.add_argument('-s', '--symbol', type=str, help='需要查询的货币，默认是所有')



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