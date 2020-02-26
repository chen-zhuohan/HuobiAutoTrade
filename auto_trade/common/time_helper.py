from datetime import datetime
import time
from configs import TIMEZONE


def now_int_timestamp(t=None):
    if t is None:
        return int(time.time())
    else:
        return int(t)


def now_format_time():
    return datetime.now(tz=TIMEZONE).strftime('%Y-%m-%d %H:%M')


def every_week_condition():
    d = datetime.now(tz=TIMEZONE)
    if d.isoweekday() == 7 and d.hour == 0 and d.minute < 5:
        return True
    return False


def every_hour_condition():
    d = datetime.now(tz=TIMEZONE)
    if d.minute < 5:
        return True
    return False


if __name__ == '__main__':
    print(now_format_time())