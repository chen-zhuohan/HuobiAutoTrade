from .admin import *

# from missions.base import MissionBase, MissionForBuy, MissionForSell
# from auto_trade.backend import DodayOpenLEMa20, VolGTVol3, WeekOpenGTNow, NowLTWeekDN, VolLTVol3Week, \
#     NowLTDayMa20, NowLTHourDN, VolGTVol3Hour, NowGTUNHour, StopLose
# from auto_trade.backend import THETAtoUSDTTrade, IOSTtoUSDTTrade
# from auto_trade.models import Trade
# from auto_trade.models import Conditions, CONDITION_TYPE
# from auto_trade.common.email_helper import send_email, send_trade
# from auto_trade.common import log
#
#
# class LongTermBuy(MissionForBuy):
#     Trade = IOSTtoUSDTTrade
#     NAME = 'first long term'
#     TASKLINE = (DodayOpenLEMa20, VolGTVol3, WeekOpenGTNow, NowLTWeekDN, VolLTVol3Week, NowLTDayMa20)
#
#
# class ShortTermBuy(MissionForBuy):
#     Trade = THETAtoUSDTTrade
#     NAME = 'feb short term'
#     TASKLINE = (NowLTHourDN, VolGTVol3Hour)
#
#
# class ShortTermSell(MissionForSell):
#     Trade = THETAtoUSDTTrade
#     NAME = 'feb short term sell'
#     TASKLINE = (NowGTUNHour, )
#
#
# class ShortTermStopLoss(MissionBase):
#     Trade = THETAtoUSDTTrade
#     NAME = 'stop feb short term'
#     TASKLINE = (StopLose, )
#
#     def do_run(self):
#         if self.pass_():
#             log.info('stop lose created')
#             send_email('止损触发', '请仔细检查账户，及时干预交易。请管理员检查定时任务是否已经关闭')
#             order = self.Trade(self.NAME).sell()
#             trade = Trade.create_by_order(order, self.NAME)
#             send_trade('成功卖出!', trade)
#             Conditions.create(type=CONDITION_TYPE.stop_lose)