# -*- coding: utf-8 -*-
import os

import logging
from app import app

app.config.from_envvar('JUST_ANOTHER_PARSER_V1_SETTINGS', silent=True)

TIMEZONE = 'Europe/Moscow'
SECRET_KEY = 'development key'
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
LOG_LEVEL = logging.DEBUG

# redis config
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

