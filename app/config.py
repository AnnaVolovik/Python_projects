# -*- coding: utf-8 -*-
import os

import logging
from app import app

app.config.from_envvar('JUST_ANOTHER_PARSER_V1_SETTINGS', silent=True)

TIMEZONE = 'Europe/Moscow'
SECRET_KEY = 'development key'
DEBUG = True
DATABASE = os.path.join(app.root_path, 'just_another_parser_v1/just_another_parser_v1.db')
SECRET_KEY = 'development key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
LOG_LEVEL = logging.DEBUG



