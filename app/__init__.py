from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('app.config')
db = SQLAlchemy(app)

# import the views when the app is initialized
from app.views import just_another_parser_v1
