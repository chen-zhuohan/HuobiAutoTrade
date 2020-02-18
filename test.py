from comm.data import data_test
from backend.mission import ShortTermBuy
import time

if __name__ == '__main__':
    start = time.time()
    for i in range(5):



        data_test()
        # ShortTermBuy().pass_(True)



    end = time.time()
    print((end-start)/5)
    # messions_test()
    # data_test()
    # # pass_test()
    # order = request_client.get_order(TRADEMATCH, 68320042418)
    # trade = Trade.create_by_order(order, 'feb short term')
    # print(trade)
    # print(data.print_object())