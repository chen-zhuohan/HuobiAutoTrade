from common.instance import db


class Task(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(64), unique=True)

    template_name = db.Column(db.VARCHAR(64))      # show for admin
    kwargs = db.Column(db.JSON)                # show for admin
    can_run = db.Column(db.VARCHAR(64))        # show for admin