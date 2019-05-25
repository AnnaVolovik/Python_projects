from flask import request, render_template
import os
import pandas as pd

from app import app


@app.route('/project_five', methods=['GET', 'POST'])
def project_five():

    filename = os.path.join(app.root_path, 'static', 'olympics.csv')
    df = pd.read_csv(filename, index_col=0, skiprows=1)
    print(df.head().to_string())
    # cleaning up the dataframe - set names where the medal pics used to go
    for col in df.columns:
        if col[:2] == '01':
            df.rename(columns={col: "Gold"+col[4:]}, inplace=True)
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
    return df.head(5).to_json()
    # return render_template('project_five.html', tables=[df.head(5).to_html(classes='data', header="true")])