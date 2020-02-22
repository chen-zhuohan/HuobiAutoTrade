from backend.mission import ShortTermBuy, ShortTermSell
from backend.trade import THETAtoUSDTTrade, IOSTtoUSDTTrade
from comm.data import data_test
from comm.huobi_client import request_client
from models.trade import Trade
import time


if __name__ == '__main__':
    # order_list = request_client.get_order_recent_48hour()
    # for order in order_list:
    #     order
    trade = THETAtoUSDTTrade(ShortTermSell.NAME)
    trade.order_id = 70721953751
    order = trade.order
    order.print_object()
    trade = Trade.create_by_order(order, ShortTermSell.NAME)
    print(trade)
    # 70721953751
    # messions_test()
    # data_test()
    # # pass_test()
    # order = request_client.get_order(TRADEMATCH, 68320042418)
    # trade = Trade.create_by_order(order, 'feb short term')
    # print(trade)
    # print(data.print_object())