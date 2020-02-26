from flask import Flask, g, Response, request, session
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from itsdangerous.jws import TimedJSONWebSignatureSerializer

from email_demo import send_email
import uuid
import configs


app = Flask(__name__)
app.config.from_object(configs)
print(app.config)
db = SQLAlchemy(app=app)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['BASIC_AUTH_FORCE'] = True
admin = Admin(app, name='火币自动交易', template_mode='bootstrap3')


class TaskPass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.SMALLINT)
    task = db.Column(db.CHAR(64), nullable=True)
    mission_start = db.Column(db.VARCHAR(64))
    mission = db.Column(db.CHAR(64))
    is_end = db.Column(db.BOOLEAN, default=False)
    result = db.Column(db.VARCHAR(255), default='')


admin.add_view(ModelView(TaskPass, db.session))


@app.before_first_request
def _init():
    db.create_all()


@app.before_request
def _before_request():
    auth = request.authorization
    if auth is None:
        pass
    elif auth.username == auth.password and auth.username == 'czh':   # first
        uuid_ = uuid.uuid4().hex
        session['login_uuid'] = uuid_
        send_email('登录验证', uuid_)
    elif session.pop('login_uuid', None) == auth.password:        # seconds
        serializer = TimedJSONWebSignatureSerializer(app.secret_key, expires_in=60)
        login_cookie = serializer.dumps({'user:': auth.username, 'password': auth.password})
        session['login_cookie'] = login_cookie
        return
    elif session.get('login_cookie'):                       # after all
        serializer = TimedJSONWebSignatureSerializer(app.secret_key, expires_in=60)
        try:
            print(serializer.loads(session['login_cookie']))
            return
        except Exception:
            print(Exception)

    return Response(status=401, headers={'WWW-Authenticate': 'Basic realm="bear"'})


@app.route('/')
def index():
    return "Hello, %s!" % getattr(g, 'user', None)


app.run(debug=True)