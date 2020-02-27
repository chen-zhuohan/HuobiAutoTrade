from common.instance import app, db
from missions.test import test_get_valid_mission_missionary, test_auto_create_missionary


# with app.app_context():
#     db.create_all()
#     db.session.execute('TRUNCATE TABLE mission')
#     db.session.execute('TRUNCATE TABLE missionary')
#     db.session.commit()
#     test_get_valid_mission_missionary()
#     test_auto_create_missionary()