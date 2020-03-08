from trade.interface import market_buy, market_sell, get_all_spot_balance, get_order


class Trade:
    BUY_CURRENCY = 'theta'
    MIDDLE_CURRENCY = 'usdt'

    def __init__(self, mission):
        self.mission = mission
        self.order_id = None
        self._order = None
        self.TRADE_MATCH = self.BUY_CURRENCY + self.MIDDLE_CURRENCY

    def get_amount(self, currency, proportion):
        amount = get_all_spot_balance(currency)
        if amount is None:
            # send_email('余额不足，无法交易', '币种： {}'.format(currency))
            raise Exception('balance is empty, cant trade')
        if proportion < 100:
            amount = amount * (proportion / 100)

        return amount

    def buy(self, proportion=100):
        amount = self.get_amount(self.MIDDLE_CURRENCY, proportion)
        self.order_id = market_buy(amount, self.TRADE_MATCH)
        return self.order

    def sell(self, proportion=100):
        amount = self.get_amount(self.BUY_CURRENCY, proportion)
        self.order_id = market_sell(amount, self.TRADE_MATCH)
        return self.order

    @property
    def order(self):
        if getattr(self, '_order', False):
            return self._order

        self._order = get_order(self.TRADE_MATCH, self.order_id)
        return self._order


class THETAtoUSDTTrade(Trade):
    BUY_CURRENCY = 'theta'
    MIDDLE_CURRENCY = 'usdt'


class IOSTtoUSDTTrade(Trade):
    BUY_CURRENCY = 'iost'
    MIDDLE_CURRENCY = 'usdt'