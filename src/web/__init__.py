from missions.interface import *
from web.login import *
from common.instance import db


@app.before_first_request
def init(*args, **kwargs):
    db.create_all()

# TODO: solute import problem