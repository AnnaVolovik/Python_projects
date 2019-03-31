# -*- coding: utf-8 -*-
from flask_script import Manager, prompt_bool, Server

from app import app, db

manager = Manager(app)


@manager.command
def init_db():
    """ Create the SQL database. """
    db.create_all()
    print('SQL Data Base has been created')

@manager.command
def drop_db():
    """ Delete SQL database  """
    if prompt_bool('Are you sure you want to delete all of your SQL data?'):
        db.drop_all()
        print('The SQL database has been deleted')

manager.add_command("runserver", Server())

if __name__ == '__main__':
    manager.run()