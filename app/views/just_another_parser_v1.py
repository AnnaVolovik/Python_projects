import os

from bs4 import BeautifulSoup
from flask import request, redirect, url_for, render_template
import requests
from requests.exceptions import MissingSchema, HTTPError

from app import app, db
from app.models import Entries
#database connections
# init_db()

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()

#view functions

#landing page - redirection to the Page 1
@app.route('/')
def index():
    return redirect(url_for('add_entry'))

#page 1
@app.route('/page_1', methods = ['GET', 'POST'])
def add_entry():
    # метод GET, отсутствуют параметры - возвращаем начальную страницу
    if request.method == 'GET':
        return render_template('page_1.html')

    # метод POST - забираем параметр URL, пробуем его распарсить
    url = request.form['url']

    try:
        r = requests.get(url)
    except MissingSchema:
        error = f'The URL does not look correct. Perhaps you meant http://{url}?'
        return render_template('page_1.html', error=error)
    except HTTPError:
        error = "Could not load the page, I'm afraid"
        return render_template('page_1.html', error=error)
    except:
        error = "Something when wrong, I must say"
        return render_template('page_1.html', error=error)

    soup = BeautifulSoup(r.content, 'lxml')
    all_tags = len(soup.findAll())
    a_tags = len(soup.findAll('a'))
    div_tags = len(soup.findAll('div'))
    entry = Entries(url=url, all_tags=all_tags, a_tags=a_tags, div_tags=div_tags)
    db.session.add(entry)
    try:

        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        return render_template('page_1.html', error='Произошла ошибка Базы Данных')
    return render_template(
        'page_1_last_entry.html', url=url, all_tags=all_tags, a_tags=a_tags, div_tags=div_tags)


#page 2 - display last 20 entries   
@app.route('/page_2')
def show_entries():
    entries = Entries.query.order_by("id desc").limit(20).all()
    return render_template('page_2.html', entries=entries)
