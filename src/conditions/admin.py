from flask_admin.contrib.sqla import ModelView
from common.instance import admin, db
from conditions.interface import Conditions

admin.add_view(ModelView(Conditions, db.session))