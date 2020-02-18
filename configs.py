from apscheduler.executors.gevent import GeventExecutor
from apscheduler.schedulers.gevent import GeventScheduler
import logging
import pytz


logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)s] - %(message)s')

TIMEZONE = pytz.timezone('Asia/Shanghai')
AccessKey = 'mn8ikls4qg-f444bdb9-825a1319-69dc6'
SecretKey = '54c7975a-453c4611-15711bf9-ba479'
url = 'api.huobi.de.com'    # 不用翻墙
# url = 'api.huobi.pro'
# url = 'api-aws.huobi.pro'


# theta是你要买的，usdt是中间火币
BUYCURRENCY = 'theta'
MIDDLECURRENCY = 'usdt'
TRADEMATCH = BUYCURRENCY + MIDDLECURRENCY

# 绑定默认的一个数据库
# SQLALCHEMY_DATABASE_URI = 'mysql://root:17081210@huobi_mysql:3306/huobi'
SQLALCHEMY_DATABASE_URI = 'postgresql://czh:17081210@118.25.56.109:5432/huobi'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 7200
SQLALCHEMY_POOL_SIZE = 100
SQLALCHEMY_POOL_TIMEOUT = 28800
SQLALCHEMY_MAX_OVERFLOW = 10


SCHEDULER_API_ENABLED = True
SCHEDULER_TIMEZONE = 'Asia/Shanghai'
SCHEDULER_EXECUTORS = {
    'default': GeventExecutor()
}
SCHEDULER_SCHEDULER = {
    'default': GeventScheduler()
}
SCHEDULER_JOB_DEFAULTS = {  # 任务的默认配置
    'coalesce': False,  # 是否允许合并任务
    'max_instances': 10,  # 任务允许的最大实例
    'misfire_grace_time': 10000  # ？
}

# celery:
CELERY_BROKER_URL = 'redis://huobi-redis:6379/0'
CELERY_RESULT_BACKEND = 'db+postgresql://czh:17081210@118.25.56.109:5432/celery'
timezone = TIMEZONE
enable_utc = False
result_expires = 60
task_time_limit = 30