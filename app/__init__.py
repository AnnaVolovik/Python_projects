from flask import Flask
from flask_redis import Redis
from flask_sqlalchemy import SQLAlchemy

# redis queue settings
# from rq import Queue
# from rq.job import Job
# from .worker import conn

app = Flask(__name__)

app.config.from_object('app.config')
db = SQLAlchemy(app)
redis = Redis(app)

# q = Queue(connection=conn)

# import the views after the app was initialized
from app.views import project_one, project_two, project_three, project_four
