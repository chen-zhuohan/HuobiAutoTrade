from flask_admin.contrib.sqla import ModelView
from common.instance import admin, db
from tasks.models.result_log import ResultLog
from tasks.models.task import Task

admin.add_view(ModelView(Task, db.session))
admin.add_view(ModelView(ResultLog, db.session))