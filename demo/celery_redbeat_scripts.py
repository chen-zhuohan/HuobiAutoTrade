from redbeat import RedBeatSchedulerEntry
from celery_redbeat_demo import celery, my_subtraction
from celery.schedules import schedule


interval = schedule(run_every=5)  # seconds
entry = RedBeatSchedulerEntry('my_subtraction', 'celery_redbeat_demo.my_add', interval, args=[5, 2], app=celery)
entry.save()