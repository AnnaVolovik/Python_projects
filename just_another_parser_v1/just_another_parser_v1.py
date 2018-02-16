import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import requests
from bs4 import BeautifulSoup
from just_another_parser_v1.database import init_db, db_session, Base
from just_another_parser_v1.models import Entries

app = Flask(__name__) 
app.config.from_object(__name__) 

#load default config 
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'just_another_parser_v1/just_another_parser_v1.db'),
    SECRET_KEY = 'development key'
    ))
app.config.from_envvar('JUST_ANOTHER_PARSER_V1_SETTINGS', silent=True)

#database connections
init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#view functions

#landing page - redirection to the Page 1
@app.route('/')
def index():
    return redirect(url_for('page_1'))

#page 1
@app.route('/page_1', methods = ['GET','POST']) 
def add_entry():
    if request.method == 'GET':
        return render_template('page_1.html')
    else:
        url = request.form['url']
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'lxml')
            all_tags = len(soup.findAll())
            a_tags = len(soup.findAll('a'))
            div_tags = len(soup.findAll('div'))
            entry = Entries(url,all_tags,a_tags,div_tags)
            db_session.add(entry)
            db_session.commit()
            return render_template('page_1_last_entry.html',url=url,all_tags=all_tags,a_tags=a_tags,div_tags=div_tags)
        except:
            error = 'Could not parse the page, please check the URL'
            return render_template('page_1.html', error=error)

#page 2 - display last 20 entries   
@app.route('/page_2')
def show_entries():
    entries = Entries.query.order_by("id desc").limit(20).all()
    return render_template('page_2.html',entries=entries)
