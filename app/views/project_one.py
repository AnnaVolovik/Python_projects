import json

from bs4 import BeautifulSoup
from flask import request
from flask_cors import cross_origin
import requests
from requests.exceptions import MissingSchema, HTTPError

from app import app, db
from app.models import Entries


@app.route('/page_1', methods=['POST'])
@cross_origin()
def add_entry():
    """Parse a url provided and return a number of tags"""
    data = request.get_json(silent=True)
    url = data.get('url')

    try:
        r = requests.get(url)
    except MissingSchema:
        error = f'The URL does not look correct. Perhaps you meant: http://{url}?'
        return json.dumps({'error':  error})
    except HTTPError:
        error = f"Could not load the page {url}"
        return json.dumps({'error': error})
    except:
        error = "Something when wrong"
        return json.dumps({'error': error})

    soup = BeautifulSoup(r.content, 'lxml')

    entry = Entries(
        url=url,
        all_tags=len(soup.findAll()),
        a_tags=len(soup.findAll('a')),
        div_tags=len(soup.findAll('div'))
    )
    db.session.add(entry)
    try:
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        return json.dumps({'error': f"An error occurred while saving data to the database"})

    res = [dict(url=url, all_tags=entry.all_tags, a_tags=entry.a_tags, div_tags=entry.div_tags)]

    return json.dumps(res)


@app.route('/page_2')
def show_entries():
    """Display last 20 entries"""
    entries = [x.as_dict() for x in Entries.query.order_by("id desc").limit(20).all()]
    return json.dumps(sorted(entries, key=lambda x: x.get('id')))
