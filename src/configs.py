import logging
import pytz
import os

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] - %(message)s')

# common:
TESTING = os.getenv('ENV', True)
timezone = 'Asia/Shanghai'
TIMEZONE = pytz.timezone(timezone)

# flask:
SECRET_KEY = 'os.urandom(24)SQLALCHEMY_POOL_TIMEOUT'

# db:
BASE_DATABASE_URI = 'postgresql://czh:17081210@118.25.56.109:5432'
SQLALCHEMY_DATABASE_URI = '{}/{}'.format(BASE_DATABASE_URI, 'test-huobi' if TESTING else 'huobi')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 7200
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_TIMEOUT = 28800
SQLALCHEMY_MAX_OVERFLOW = 10

# celery:
REDIS_URL = 'redis://huobi-redis:6379/0' if not TESTING else 'redis://127.0.0.1:6379/0'
broker_url = REDIS_URL
redbeat_redis_url = REDIS_URL
result_backend = 'db+{}/{}'.format(BASE_DATABASE_URI, 'test-celery' if TESTING else 'celery')
task_ignore_result = True
task_store_errors_even_if_ignored = True
enable_utc = False
result_expires = 60
task_time_limit = 30

# huobi:
AccessKey = 'mn8ikls4qg-f444bdb9-825a1319-69dc6'
SecretKey = '54c7975a-453c4611-15711bf9-ba479'
HUOBI_URL = 'https://api.huobi.de.com'    # 不用翻墙
# HUOBI_URL = 'https://api.huobi.pro'
# HUOBI_URL = 'https://api-aws.huobi.pro'
MARKET_KLINE_URL = HUOBI_URL + '/market/history/kline'
# theta是你要买的，usdt是中间火币
BUY_CURRENCY = 'theta'
MIDDLE_CURRENCY = 'usdt'
TRADE_MATCH = BUY_CURRENCY + MIDDLE_CURRENCY

# login & email:
USERS = {
    'czh': '1185671574@qq.com'
} if TESTING else {
    'czh': '1185671574@qq.com',
    'hjr': '1582544942@qq.com'
}
LOGIN_EXPIRES_IN = 2592000
MAIL_HOST = "smtp.qq.com"  # 设置服务器
MAIL_USER = "1185671574@qq.com"  # 用户名
MAIL_PASSWORD = "fjrhahmxiavgidei"  # 口令
MAIL_PORT = 587