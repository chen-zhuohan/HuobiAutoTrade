from comm.huobi_client import market_buy, market_sell, get_all_spot_balance, get_order


class Trade:
    BUYCURRENCY = 'theta'
    MIDDLECURRENCY = 'usdt'

    def __init__(self, mission):
        self.mission = mission
        self.order_id = None
        self._order = None
        self.TRADEMATCH = self.BUYCURRENCY + self.MIDDLECURRENCY

    def get_amount(self, currency, proportion):
        amount = get_all_spot_balance(currency)
        if amount is None:
            # send_email('余额不足，无法交易', '币种： {}'.format(currency))
            raise Exception('balance is empty, cant trade')
        if proportion < 100:
            amount = amount * (proportion / 100)

        return amount

    def buy(self, proportion=100):
        amount = self.get_amount(self.MIDDLECURRENCY, proportion)
        self.order_id = market_buy(amount, self.TRADEMATCH)
        return self.order

    def sell(self, proportion=100):
        amount = self.get_amount(self.BUYCURRENCY, proportion)
        self.order_id = market_sell(amount, self.TRADEMATCH)
        return self.order

    @property
    def order(self):
        if getattr(self, '_order', False):
            return self._order

        self._order = get_order(self.TRADEMATCH, self.order_id)
        return self._order


class THETAtoUSDTTrade(Trade):
    BUYCURRENCY = 'theta'
    MIDDLECURRENCY = 'usdt'


class IOSTtoUSDTTrade(Trade):
    BUYCURRENCY = 'IOST'
    MIDDLECURRENCY = 'usdt'