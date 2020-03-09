from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField

from common.admin_help import json_formatter, JSONField
from common.instance import admin, db
from tasks.constant import TASK_TYPE
from tasks.engine import task_template_dict
from tasks.models.result_log import ResultLog
from tasks.models.task import Task


class MyView(ModelView):
    def validate_form(self, form):
        form.pref1.data = int(form.status.data)
        return super(MyView, self).validate_form(form)

    def on_form_prefill(self, form, id):
        form.pref1.data = str(form.pref1.data)  # in Python 2, use the unicode function instead

class TaskViewModel(ModelView):
    column_list = ['id', 'name', 'template_name', 'kwargs', 'run_time', 'can_run', 'type']
    """form_choices = {'my_form_field': [
            ('db_value', 'display_value'),
        ]}"""
    form_overrides = {
        'kwargs': JSONField,
        # 'type': SelectField
    }
    #
    # form_args = {
    #     'type': {'choices': [(int(key), value) for key, value in TASK_TYPE.items()], 'coerce': int}
    # }
    form_choices = {
        'template_name': [(key, obj.RULE + obj.get_args()) for key, obj in task_template_dict.items()],
        'type': [(key, value) for key, value in TASK_TYPE.items()]
    }
    column_sortable_list = ['name']
    column_editable_list = ['type', 'can_run', 'name']
    column_formatters = {
        'kwargs': json_formatter,
    }

    def validate_form(self, form):
        form.type.data = int(form.type.data)
        return super(TaskViewModel, self).validate_form(form)

    def on_form_prefill(self, form, id):
        form.type.data = str(form.type.data)  # in Python 2, use the unicode function instead


admin.add_view(TaskViewModel(Task, db.session))
admin.add_view(ModelView(ResultLog, db.session))