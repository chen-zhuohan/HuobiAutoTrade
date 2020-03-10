from celery.schedules import schedule, crontab
from collections import OrderedDict
from datetime import datetime
import time

from common.utils import Logger
from configs import TIMEZONE

logger = Logger('TIME HELPER')

def can_run_1min():
    logger.info('1 min always return True')
    return True

def can_run_5min():
    logger.info('to konw 5 min if can run or not')
    return datetime.now(tz=TIMEZONE).minute // 5 == 0

def can_run_15min():
    logger.info('to konw 15 min if can run or not')
    return datetime.now(tz=TIMEZONE).minute // 15 == 0

def can_run_30min():
    logger.info('to konw 30 min if can run or not')
    return datetime.now(tz=TIMEZONE).minute // 30 == 0

def can_run_60min():
    logger.info('to konw 60 min if can run or not')
    return datetime.now(tz=TIMEZONE).minute in (0, 1)

def can_run_4h():
    logger.info('to konw 4 h if can run or not')
    return datetime.now(tz=TIMEZONE).hour // 4 == 0

def can_run_1day():
    logger.info('to konw 1 day if can run or not')
    return datetime.now(tz=TIMEZONE).hour == 0 and can_run_60min()


RUN_TIME_CHOICE = ['1min', '5min', '15min', '30min', '60min', '4hour', '1day']
CAN_RUN_TIME_FUNC = {
    '1min': can_run_1min,
    '5min': can_run_5min,
    '15min': can_run_15min,
    '30min': can_run_30min,
    '60min': can_run_60min,
    '4hour': can_run_4h,
    '1day': can_run_1day
}
RUN_TIME_SCHEDULE = {
    '1min': schedule(run_every=60),  # seconds,
    '5min': crontab(minute='*/5'),
    '15min': crontab(minute='*/15'),
    '30min': crontab(minute='*/30'),
    '60min': crontab(minute='*/60'),
    # '60min': schedule(run_every=60),
    '4hour': crontab(minute='0', hour='*/4'),
    '1day': crontab(minute='0', hour='0')
}


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


def can_run_at_now(a, now=''):
    if now == '':                 # first run missionary, no value
        logger.info('can run return True due to now is blank str')
        return True

    if a not in RUN_TIME_CHOICE or now not in RUN_TIME_CHOICE:
        error_info = 'a, now limit in line: {}, but received a: {}, b: {}'.format(RUN_TIME_CHOICE, a, now)
        logger.error(error_info)
        raise ValueError(error_info)

    if RUN_TIME_CHOICE.index(a) <= RUN_TIME_CHOICE.index(now):
        logger.info('can run return True due to a less than now')
        return True

    result = CAN_RUN_TIME_FUNC[a]()
    logger.info('can run return {} due to CAN RUN TIME FUNC'.format(result))
    return result


if __name__ == '__main__':
    print(now_format_time())