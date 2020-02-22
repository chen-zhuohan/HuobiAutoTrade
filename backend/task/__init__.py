from backend.task.normal import DodayOpenLEMa20, VolGTVol3, WeekOpenGTNow, NowLTWeekDN, VolLTVol3Week, \
    NowLTDayMa20, NowLTHourDN, VolGTVol3Hour, NowGTUNHour, StopLose


def messions_test():
    m = DodayOpenLEMa20()
    print(m.pass_(True))