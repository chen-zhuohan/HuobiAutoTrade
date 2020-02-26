# from auto_trade.common import every_hour_condition, every_week_condition
# from auto_trade.common.data import DataPool
# from auto_trade.backend import TaskBase
# from auto_trade.models import Trade
#
#
# class DodayOpenLEMa20(TaskBase):
#     RULE = '第0阶段第1次判断：这周开盘价应该在ma20上下10%的闭区间内。（每周日00：01执行）'
#     MSG = 'ma20为 {} 上下浮动10%的区间是 {} - {} ，这周的开盘价是 {} '
#
#     def run_condition(self):
#         return every_week_condition()
#
#     def pass_condition(self):
#         last_21_weeks = DataPool.BTCtoUSDT.Weeks21()
#         today_open = last_21_weeks[0]['open']
#         ma20 = DataPool.BTCtoUSDT.OpenMA20Weeks()
#         open_min = ma20 * 0.90
#         open_max = ma20 * 1.10
#         self.msg_arg = (ma20, open_min, open_max, today_open)
#
#         if open_min <= today_open <= open_max:
#             return True
#         return False
#
#
# class VolGTVol3(TaskBase):
#     RULE = '第0阶段第2次判断：上一周交易总量应该大于前三周交易总量的均值。（每周日00：01执行）'
#     MSG = '上一周的交易总量是 {}， 上三周的交易均值是 {}'
#
#     def run_condition(self):
#         return every_week_condition()
#
#     def pass_condition(self):
#         last_vol, vol3 = DataPool.BTCtoUSDT.VolaVol3Week()
#         self.msg_arg = (last_vol, vol3)
#
#         if last_vol > vol3:
#             return True
#         return False
#
#
# class WeekOpenGTNow(TaskBase):
#     RULE = '第0阶段第3次判断：现价（收盘价）应该低于这周开盘价。（一直执行）'
#     MSG = '这周开盘价 {}， 现价（收盘价） {}'
#
#     def run_condition(self):
#         return True
#
#     def pass_condition(self):
#         now_week = DataPool.BTCtoUSDT.WeekNow()
#         open_, close = now_week[0]['open'], now_week[0]['close']
#         self.msg_arg = (open_, close)
#
#         if open_ > close:
#             return True
#         return False
#
#
# class NowLTWeekDN(TaskBase):
#     RULE = '第1阶段第1次判断：现价（收盘价）应该低于布林下轨。（每周日00：01执行）'
#     MSG = '现价（收盘价）为 {}， 布林下轨为 {}'
#
#     def run_condition(self):
#         return every_week_condition()
#
#     def pass_condition(self):
#         close = DataPool.BTCtoUSDT.NowPrice()
#         DN = DataPool.BTCtoUSDT.WeekDN()
#         self.msg_arg = (close, DN)
#
#         if close < DN:
#             return True
#         return False
#
#
# class VolLTVol3Week(TaskBase):
#     RULE = '第1阶段第2次判断：上周交易总量应该低于前三周交易总量的均值。（每周日00：01执行）'
#     MSG = '上一周的交易总量是 {}， 上三周的交易均值是 {}'
#
#     def run_condition(self):
#         return every_week_condition()
#
#     def pass_condition(self):
#         last_vol, vol3 = DataPool.BTCtoUSDT.VolaVol3Week()
#         self.msg_arg = (last_vol, vol3)
#
#         if last_vol < vol3:
#             return True
#         return False
#
#
# class NowLTDayMa20(TaskBase):
#     RULE = '第2阶段第1次判断：现价（收盘价）应该低于ma20（单位：天）。（一直执行）'
#     MSG = '现价（收盘价） {}， ma20（单位：天） {}'
#
#     def run_condition(self):
#         return True
#
#     def pass_condition(self):
#         now = DataPool.BTCtoUSDT.NowPrice()
#         ma20 = DataPool.BTCtoUSDT.OpenMA20Days()
#         self.msg_arg = (now, ma20)
#
#         if now < ma20:
#             return True
#         return False
#
#
# class NowLTHourDN(TaskBase):
#     RULE = '短期第0阶段第1次判断：这一小时的现价（收盘价）应该低于DN。（每小时00：01执行'
#     MSG = '这小时的现价是 {}, DN为 {}'
#
#     def run_condition(self):
#         return every_hour_condition()
#
#     def pass_condition(self):
#         close = DataPool.THETAtoUSDT.NowPrice()
#         DN = DataPool.THETAtoUSDT.HourDN()
#         self.msg_arg = (close, DN)
#
#         if close < DN:
#             return True
#         return False
#
#
# class VolGTVol3Hour(TaskBase):
#     RULE = '短期第0阶段第2次判断：上一小时交易总量应该大于前三小时交易总量的均值。（每小时00：01执行）'
#     MSG = '上一小时的交易总量是 {}， 上三小时的交易均值是 {}'
#
#     def run_condition(self):
#         return every_hour_condition()
#
#     def pass_condition(self):
#         last_vol, vol3 = DataPool.THETAtoUSDT.VolaVol3Hour()
#         self.msg_arg = (last_vol, vol3)
#
#         if last_vol > vol3:
#             return True
#         return False
#
#
# class NowGTUNHour(TaskBase):
#     RULE = '短期卖出判断：当前价格高于UN。（每小时00：01执行）'
#     MSG = '当前价格是 {}，UN是 {}'
#
#     def run_condition(self):
#         return every_hour_condition()
#
#     def pass_condition(self):
#         now = DataPool.THETAtoUSDT.NowPrice()
#         un = DataPool.THETAtoUSDT.HourUN()
#         self.msg_arg = (now, un)
#
#         if now > un:
#             return True
#         return False
#
#
# class StopLose(TaskBase):
#     RULE = '买入价格和现价的差值占上个小时收盘价的3%（一直执行）'
#     MSG = '买入价格 {}， 现价 {}， 差价 {}， 上个小时收盘价 {}, 比值 {}'
#
#     def run_condition(self):
#         return True
#
#     def pass_condition(self):
#         last_trade = Trade.get_last(mission='feb short term', type='buy-market')
#         if last_trade is None:
#             self.msg_arg = (0, 0, 0, 0, 0)
#             return False
#
#         buy_price = float(last_trade.price)
#         now_price = DataPool.THETAtoUSDT.NowPrice()
#         last_hour_price = DataPool.THETAtoUSDT.Hours21()[1]['close']
#         diff = buy_price - now_price
#         p = diff/last_hour_price
#         self.msg_arg = (buy_price, now_price, diff, last_hour_price, p)
#         if diff > 0 and p > 0.03:
#             return True
#
#         return False