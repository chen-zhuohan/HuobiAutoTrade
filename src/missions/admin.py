from flask_admin.contrib.sqla import ModelView
from common.instance import admin, db
from missions.model import Mission, Missionary

admin.add_view(ModelView(Mission, db.session))
admin.add_view(ModelView(Missionary, db.session))