from flask import Flask
from flask_redis import Redis
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# redis queue settings
# from rq import Queue
# from rq.job import Job
# from .worker import conn

app = Flask(__name__)
CORS(app)

app.config.from_object('app.config')
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
redis = Redis(app)

# q = Queue(connection=conn)

# import the views after the app was initialized
from app.views import project_one, project_two, project_three, project_four, project_five
