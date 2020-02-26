import logging
import pytz
import os


logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] - %(message)s')


# common:
TEST = True
timezone = 'Asia/Shanghai'
TIMEZONE = pytz.timezone(timezone)

# flask:
SECRET_KEY = 'os.urandom(24)SQLALCHEMY_POOL_TIMEOUT'

# db:
BASE_DATABASE_URI = 'postgresql://czh:17081210@118.25.56.109:5432'
SQLALCHEMY_DATABASE_URI = '{}/{}'.format(BASE_DATABASE_URI, 'test-huobi' if TEST else 'huobi')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 7200
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_TIMEOUT = 28800
SQLALCHEMY_MAX_OVERFLOW = 10

# celery:
redis_url = 'redis://huobi-redis:6379/0' if not TEST else 'redis://127.0.0.1:6379/0'
broker_url = redis_url
redbeat_redis_url = redis_url
result_backend = 'db+{}/{}'.format(BASE_DATABASE_URI, 'test-celery' if TEST else 'celery')
enable_utc = False
result_expires = 60
task_time_limit = 30

# huobi:
AccessKey = 'mn8ikls4qg-f444bdb9-825a1319-69dc6'
SecretKey = '54c7975a-453c4611-15711bf9-ba479'
url = 'api.huobi.de.com'    # 不用翻墙
# url = 'api.huobi.pro'
# url = 'api-aws.huobi.pro'
# theta是你要买的，usdt是中间火币
BUY_CURRENCY = 'theta'
MIDDLE_CURRENCY = 'usdt'
TRADE_MATCH = BUY_CURRENCY + MIDDLE_CURRENCY