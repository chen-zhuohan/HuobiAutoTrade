from backend.mission.base import MissionBase, MissionForBuy, MissionForSell
from backend.task import DodayOpenLEMa20, VolGTVol3, WeekOpenGTNow, NowLTWeekDN, VolLTVol3Week, \
    NowLTDayMa20, NowLTHourDN, VolGTVol3Hour, NowGTUNHour, StopLose
from backend.trade import THETAtoUSDTTrade, IOSTtoUSDTTrade
from models.trade import Trade
from models.conditions import Conditions, CONDITION_TYPE
from comm.email_helper import send_email, send_trade
from comm.instance import log


class LongTermBuy(MissionForBuy):
    Trade = IOSTtoUSDTTrade
    NAME = 'first long term'
    TASKLINE = (DodayOpenLEMa20, VolGTVol3, WeekOpenGTNow, NowLTWeekDN, VolLTVol3Week, NowLTDayMa20)


class ShortTermBuy(MissionForBuy):
    Trade = THETAtoUSDTTrade
    NAME = 'feb short term'
    TASKLINE = (NowLTHourDN, VolGTVol3Hour)


class ShortTermSell(MissionForSell):
    Trade = THETAtoUSDTTrade
    NAME = 'feb short term sell'
    TASKLINE = (NowGTUNHour, )


class ShortTermStopLoss(MissionBase):
    Trade = THETAtoUSDTTrade
    NAME = 'stop feb short term'
    TASKLINE = (StopLose, )

    def do_run(self):
        if self.pass_():
            log.info('stop lose created')
            send_email('止损触发', '请仔细检查账户，及时干预交易。请管理员检查定时任务是否已经关闭')
            order = self.Trade(self.NAME).sell()
            trade = Trade.create_by_order(order, self.NAME)
            send_trade('成功卖出!', trade)
            Conditions.create(type=CONDITION_TYPE.stop_lose)