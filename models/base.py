from sqlalchemy import desc

from comm.instance import db
from comm.time_helper import now_format_time, now_int_timestamp


class UpdateBase:
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.VARCHAR(64), default=now_format_time)
    timestamp = db.Column(db.Integer, default=now_int_timestamp)

    @classmethod
    def create(cls, **kwargs):
        ret = cls()
        ret.update(data=kwargs)
        return ret

    def update(self, data):
        for k in data:
            if k != 'id':
                setattr(self, k, data[k])
        self.save()

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            print("DB", "sql commit error info", {'error': str(e)})
            db.session.rollback()

    @classmethod
    def get_last(cls, **kwargs):
        return cls.query.filter_by(**kwargs).order_by(desc(cls.id)).limit(1).first()