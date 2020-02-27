# from common.data.pool import DataPool
#
#
# def data_test():
#     for match in [DataPool.BTCtoUSDT, DataPool.THETAtoUSDT]:
#         for data_key in match.__dict__:
#             print(match, data_key)
#             print('='*10, data_key, '='*10)
#             print(getattr(match, data_key)())
    # print(DataPool.THETAtoUSDT.OpenMA20Weeks())
    # print('=' * 20)
    # print(DataPool.BTCtoUSDT.OpenMA20Weeks())
    # print('=' * 20)
    # print(DataPool.BTCtoUSDT.Weeks21())
    # print('=' * 20)
    # print(DataPool.BTCtoUSDTOpenMA20Weeks())
    # print('=' * 20)
    # print(DataPool.BTCtoUSDTWeekDN())
    # print('=' * 20)
    # print(DataPool.BTCtoUSDTNowPrice())
    # print('=' * 20)
    # print(DataPool.BTCtoUSDTVolaVol3Week())