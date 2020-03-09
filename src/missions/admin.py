from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2TagsField

from common.instance import admin, db
from missions.model import Mission, Missionary


class Select2IntegerTagsField(Select2TagsField):
    def process_formdata(self, valuelist):
        super().process_formdata(valuelist)
        self.data = [int(x) for x in self.data]


class MissionModelView(ModelView):
    column_list = ['id', 'name', 'task_line', 'is_valid', 'next_run_mission']
    column_editable_list = ['name', 'is_valid', 'next_run_mission']

    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.task_line = Select2IntegerTagsField("Task Line", save_as_list=True)
        return form_class


admin.add_view(MissionModelView(Mission, db.session))
admin.add_view(ModelView(Missionary, db.session))