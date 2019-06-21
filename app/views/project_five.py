from flask import request, render_template
import os
import pandas as pd

from flask.ext.cache import Cache

from app import app
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@cache.cached(timeout=600)
def get_df():
    """Get a dataframe from a csv file and clean it up"""
    filename = os.path.join(app.root_path, 'static', 'olympics.csv')
    df = pd.read_csv(filename, index_col=0, skiprows=1)

    # cleaning up the dataframe - set names where the medal pics used to go
    for col in df.columns:
        if col[:2] == '01':
            df.rename(columns={col: "Gold" + col[4:]}, inplace=True)
        if col[:2] == '02':
            df.rename(columns={col: 'Silver' + col[4:]}, inplace=True)
        if col[:2] == '03':
            df.rename(columns={col: 'Bronze' + col[4:]}, inplace=True)
        if col[:1] == '№':
            df.rename(columns={col: '#' + col[1:]}, inplace=True)

    names_ids = df.index.str.split('\s\(')
    df.index = names_ids.str[0]  # the [0] element is the country name (new index)
    df['ID'] = names_ids.str[1].str[:3]  # the [1] element is the abbreviation or ID (take first 3 characters from that)

    df = df.drop('Totals')

    return df


@app.route('/get_entire_df', methods=['GET'])
def get_entire_df():
    """Return the entire dataframe"""
    df = get_df()
    return df.to_json()


@app.route('/get_only_gold', methods=['GET'])
def get_only_gold():
    """Return only the gold winner countries"""
    df = get_df()
    only_gold = df[df['Gold'] > 0]
    only_gold = only_gold.dropna()
    return only_gold.to_json()
