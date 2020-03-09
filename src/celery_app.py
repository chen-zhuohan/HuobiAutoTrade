from common.instance import celery
from common.utils import Logger
from missions.interface import run_mission, get_valid_mission_missionary
from schedule.interface import add_missionary, add_all_missionary

log = Logger('MY APS')

add_all_missionary()



# celery -A celery_main beat --loglevel=info
# celery -A celery_main worker --loglevel=info