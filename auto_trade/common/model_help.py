from sqlalchemy import desc

from common.instance import db
from common.email_helper import send_error
from common.time_helper import now_format_time, now_int_timestamp
from common.utils import Logger


log = Logger('BASE MODEL')


def safe_commit():
    try:
        db.session.commit()
    except Exception as e:
        log.error("DB sql commit error, detail: {}, {}".format(e, e.args))
        send_error(e, 'db commit')
        db.session.rollback()


def save_many_models(*args):
    for model in args:
        db.session.add(model)
    safe_commit()


class UpdateModelBase(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.VARCHAR(64), default=now_format_time)
    timestamp = db.Column(db.Integer, default=now_int_timestamp)
    update_time = db.Column(db.Integer, onupdate=now_int_timestamp)

    def save(self):
        db.session.add(self)
        safe_commit()
        return self

    @classmethod
    def get_last(cls, **kwargs):
        return cls.query.filter_by(**kwargs).order_by(desc(cls.id)).limit(1).first()


