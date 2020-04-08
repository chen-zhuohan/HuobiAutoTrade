from flask_sqlalchemy import models_committed
from sqlalchemy import event

from common.model_help import UpdateModelBase
from common.time_helper import now_int_timestamp
from common.instance import db
from tasks.interface import get_task_run_time_by_id
# from schedule.interface import update_missionary, del_missionary, add_missionary


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
    is_valid = db.Column(db.Boolean, server_default='t')
    next_run_mission = db.Column(db.INTEGER, nullable=True)

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

    run_time = db.Column(db.VARCHAR(64), server_default='', nullable=False)
    is_end = db.Column(db.BOOLEAN, server_default='f')
    end_time = db.Column(db.Integer, server_default='0')
    result_log_id = db.Column(db.Integer, server_default='0')

    def add_task_index(self, save=True):
        self.next_task_index += 1
        if save:
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
    def create_by_mission(cls, mission: Mission):
        if len(mission.task_line) > 0:
            first_task_id = mission.task_line[0]
            run_time = get_task_run_time_by_id(first_task_id)
        else:
            run_time = '1min'
        return cls(mission_id=mission.id, run_time=run_time).save()

    @classmethod
    def get_or_create_by_mission(cls, mission):
        None_able = cls.query.filter_by(mission_id=mission.id, is_end=False).first()
        if None_able is None:
            return cls.create_by_mission(mission)
        return None_able

    @classmethod
    def get_valid_mission_id_to_missionary(cls):
        result = {}
        for missionary in cls.query.filter_by(is_end=False).all():
            result[missionary.mission_id] = missionary
        return result


# @event.listens_for(Mission, 'after_update')
# def my_append_listener(mapper, connect, instance: Mission):
#     if instance.is_valid:
#         update_missionary(mission=instance)
#     else:
#         del_missionary(instance.id)


# @models_committed.connect
# def on_models_committed(*args, **kwargs):
#     print(*args)
#     print(**kwargs)
    # for obj, change in changes:
    #     if change == 'insert' and hasattr(obj, '__commit_insert__'):
    #         obj.__commit_insert__()
    #     elif change == 'update' and hasattr(obj, '__commit_update__'):
    #         obj.__commit_update__()
    #     elif change == 'delete' and hasattr(obj, '__commit_delete__'):
    #         obj.__commit_delete__()