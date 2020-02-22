from apscheduler.events import SchedulerEvent
from redbeat import RedBeatSchedulerEntry

from backend.mission import LongTermBuy, ShortTermBuy, ShortTermSell, ShortTermStopLoss
from comm.instance import celery
from comm.utils import Logger
RedBeatSchedulerEntry

log = Logger('MY APS')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, run_ShortTermBuy.s())
    sender.add_periodic_task(60.0, run_LongTermBuy.s())
    sender.add_periodic_task(60.0, run_ShortTermSell.s())
    sender.add_periodic_task(60.0, run_ShortTermStopLoss.s())


@celery.task(name='短期买入')
def run_ShortTermBuy():
    ShortTermBuy.run().last_result.short_str


@celery.task(name='长期买入')
def run_LongTermBuy():
    LongTermBuy.run().last_result.short_str


@celery.task(name='短期卖出')
def run_ShortTermSell():
    ShortTermSell.run().last_result.short_str


@celery.task(name='短期止损')
def run_ShortTermStopLoss():
    ShortTermStopLoss.run().last_result.short_str


# celery -A celery_main beat --loglevel=info
# celery -A celery_main worker --loglevel=info