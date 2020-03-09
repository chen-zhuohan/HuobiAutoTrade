from common.instance import db
from tasks.constant import TASK_TYPE_CLASS


class Task(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(64), nullable=True)

    type = db.Column(db.INTEGER, server_default=str(TASK_TYPE_CLASS.Data))
    template_name = db.Column(db.VARCHAR(64))       # show for admin
    kwargs = db.Column(db.JSON)                     # show for admin
    can_run = db.Column(db.VARCHAR(64))             # show for admin

    run_time = db.Column(db.VARCHAR(64))