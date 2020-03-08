from flask_admin.contrib.sqla import ModelView
from common.instance import admin, db
from trade.model import Trade

admin.add_view(ModelView(Trade, db.session))