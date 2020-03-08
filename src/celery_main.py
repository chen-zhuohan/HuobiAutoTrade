from common.instance import celery
from common.utils import Logger
from missions.interface import run_mission, get_valid_mission_missionary
from schedule.interface import add_missionary

log = Logger('MY APS')





# celery -A celery_main beat --loglevel=info
# celery -A celery_main worker --loglevel=info