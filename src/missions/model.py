from common.model_help import UpdateModelBase
from common.time_helper import now_int_timestamp
from common.instance import db


class Mission(UpdateModelBase):
    name = db.Column(db.VARCHAR(64), unique=True)
    # task id
    target = db.Column(db.Integer)
    # task id list
    task_line = db.Column(db.ARRAY(db.Integer, zero_indexes=True))
    # condition name
    can_run_before_each_task = db.Column(db.VARCHAR(64), server_default='')
    can_run_before_target = db.Column(db.VARCHAR(64), server_default='')

    # for celery
    run_time = db.Column(db.JSON, server_default='{"minute": 0, "hour": "*"}')
    is_valid = db.Column(db.Boolean, server_default='t')

    def __str__(self):
        return '[{} is valid: {}]'.format(self.name, self.is_valid)

    @classmethod
    def get_valid_missions(cls):
        return cls.query.filter_by(is_valid=True).all()

    @classmethod
    def get_valid_mission_id_line(cls):
        result = []
        for mission in cls.query.filter_by(is_valid=True).with_entities('id').all():
            result.append(mission[0])
        return result


class Missionary(UpdateModelBase):
    mission_id = db.Column(db.Integer)
    next_task_index = db.Column(db.Integer, server_default='0')

    is_end = db.Column(db.BOOLEAN, server_default='f')
    end_time = db.Column(db.Integer, server_default='0')
    result_log_id = db.Column(db.Integer, server_default='0')

    def add_next_task_index(self):
        self.next_task_index += 1
        self.save()

    def finish(self):
        self.is_end = True
        self.end_time = now_int_timestamp()
        self.save()

    @classmethod
    def create(cls, mission_id):
        return cls(mission_id=mission_id).save()

    def create_new_after_finish(self):
        self.create(self.mission_id)

    @classmethod
    def create_by_mission(cls, mission):
        return cls(mission_id=mission.id).save()

    @classmethod
    def get_or_create_by_mission(cls, mission):
        None_able = cls.query.filter_by(mission_id=mission.id).first()
        if None_able is None:
            return cls.create_by_mission(mission)
        return None_able

    @classmethod
    def get_valid_mission_id_to_missionary(cls):
        result = {}
        for missionary in cls.query.filter_by(is_end=False).all():
            result[missionary.mission_id] = missionary
        return result