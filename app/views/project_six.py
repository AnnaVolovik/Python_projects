import os

from flask.ext.cache import Cache
import inspect
import json
import pandas as pd
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from scipy.stats import ttest_ind

from app import app


class HypothesisTesting:

    """Demonstrating the ability to acquire, manipluate, clean and run basic data analysis.
     Providing evidence for (or against!) a given hypothesis as part of "Introduction to Data Science in Python"
     Coursera course by University of Michigan."""

    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National',
              'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana',
              'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho',
              'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan',
              'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi',
              'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota',
              'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut',
              'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York',
              'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado',
              'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota',
              'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
              'ND': 'North Dakota', 'VA': 'Virginia'}

    def get_list_of_university_towns(self):
        """Returns a DataFrame of towns and the states they are in from the
        university_towns.txt list. The format of the DataFrame should be:
        DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
        columns=["State", "RegionName"]  )

        The following cleaning needs to be done:

        1. For "State", removing characters from "[" to the end.
        2. For "RegionName", when applicable, removing every character from " (" to the end.
        3. Depending on how you read the data, you may need to remove newline character '\n'. """
        filename = os.path.join(app.root_path, 'static', 'university_towns.txt')
        df = pd.read_csv(filename, delimiter="\t", header=None)
        res = []
        for row in df.iterrows():
            if row[1][0].endswith("[edit]"):
                state = row[1][0].replace("[edit]", "")
            else:
                res.append([state, row[1][0].split('(')[0].strip()])

        self.Towns = pd.DataFrame(res, columns=["State", "RegionName"])
        return self.Towns

    def get_gdp_data(self):
        """ Retrieve GDP data from the first quarter of 2000 onward from the gdplev.xls file, provided by Bureau of
        Economic Analysis, US Department of Commerce. Use the chained value in 2009 dollars, in quarterly intervals.
        """
        filename = os.path.join(app.root_path, 'static', 'gdplev.xls')
        self.GDP = (pd.read_excel(filename,
                             skiprows=list(range(0, 5, 1)) + list(range(6, 220, 1)),
                             usecols=[4, 6], names=['Quarterly intervals', 'GDP']).set_index('Quarterly intervals')
                    )

        return self.GDP

    @staticmethod
    def get_recession_start_or_end(data, action):
        """A helper function on defining recession time frames"""
        x = data.iloc[0, 0]
        saved_index = None

        for index, row in data.iterrows():
            if row['GDP'] < x if action == 'start' else row['GDP'] > x:
                if saved_index:
                    if action == 'start':
                        res = saved_index
                    else:
                        res = index
                    break
                else:
                    saved_index = index
            elif saved_index:
                saved_index = None
            x = row['GDP']

        return res

    def get_recession_start(self):
        """Returns the year and quarter of the recession start time as a
        string value in a format such as 2005q3"""
        self.recession_start = self.get_recession_start_or_end(self.GDP, 'start')
        return self.recession_start

    def get_recession_end(self):
        """Returns the year and quarter of the recession end time as a
        string value in a format such as 2005q3"""
        self.recession_end = self.get_recession_start_or_end(self.GDP.loc[self.recession_start:], 'end')
        return self.recession_end

    def get_recession_bottom(self):
        """Returns the year and quarter of the recession bottom time as a
        string value in a format such as 2005q3"""
        self.recession_bottom = self.GDP.loc[self.recession_start:self.recession_end].idxmin()[0]
        return self.recession_bottom


    def convert_housing_data_to_quarters(self):
        """Converts the housing data to quarters and returns it as mean
        values in a dataframe. This dataframe should be a dataframe with
        columns for 2000q1 through 2016q3, and should have a multi-index
        in the shape of ["State","RegionName"].

        Note: Quarters are defined in the assignment description, they are
        not arbitrary three month periods.

        The resulting dataframe should have 67 columns, and 10,730 rows.
        """
        filename = os.path.join(app.root_path, 'static', 'City_Zhvi_AllHomes.csv')
        df = pd.read_csv(filename, usecols=[1, 2] + list(range(51, 251, 1)))
        newData = df[["State", "RegionName"]]
        newData['State'] = newData['State'].map(lambda x: self.states.get(x))
        cols = ["{}q{}".format(x, y) for x in range(2000, 2017, 1) for y in range(1, 5, 1)]
        start = 2
        for quarter_index in cols[:-1]:
            newData[quarter_index] = df.iloc[:, start:start + 3].mean(axis=1)
            start += 3
        self.HousingData = newData.set_index(["State", "RegionName"])
        return self.HousingData


    def run_ttest(self):
        """First creates new data showing the decline or growth of housing prices
        between the recession start and the recession bottom. Then runs a ttest
        comparing the university town values to the non-university towns values,
        return whether the alternative hypothesis (that the two groups are the same)
        is true or not as well as the p-value of the confidence.

        Return the tuple (different, p, better) where different=True if the t-test is
        True at a p<0.01 (we reject the null hypothesis), or different=False if
        otherwise (we cannot reject the null hypothesis). The variable p should
        be equal to the exact p value returned from scipy.stats.ttest_ind(). The
        value for better should be either "university town" or "non-university town"
        depending on which has a lower mean price ratio (which is equivilent to a
        reduced market loss)."""

        df = self.HousingData.loc[:, self.recession_start: self.recession_bottom].reset_index()
        df['price_ratio'] = (df[self.recession_start] - df[self.recession_bottom]).div(
            df[self.recession_start])

        df['is_university_towm'] = df.RegionName.apply(lambda x: x in self.Towns['RegionName'].tolist())
        university_towns = df[df.is_university_towm].dropna()['price_ratio']
        non_university_towns = df[~df.is_university_towm].dropna()['price_ratio']
        res = ttest_ind(university_towns, non_university_towns)
        lower = 'university town' if university_towns.mean() < non_university_towns.mean() else 'non-university town'
        return res[1] < 0.01, res[1], lower


ins = HypothesisTesting()
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def source_code_to_html(func):
    """Present function source code as HTML"""
    code = inspect.getsource(func)
    return highlight(code, PythonLexer(), HtmlFormatter(style='algol', lineseparator='<br />'))


@app.route('/get_hypothesis_testing_functions', methods=['GET'])
@cache.cached(timeout=600)
def get_hypothesis_testing_functions():
    """Return source code and results to the front end"""
    res = {}
    # functions_in_order = ['get_gdp_data', 'get_recession_start']
    functions_in_order = ['get_list_of_university_towns', 'get_gdp_data', 'get_recession_start_or_end',
                          'get_recession_start', 'get_recession_end', 'get_recession_bottom',
                          'convert_housing_data_to_quarters', 'run_ttest']
    member_functions = {o[0]: o[1] for o in inspect.getmembers(HypothesisTesting)}

    for f_name in functions_in_order:

        res[f_name] = dict()
        f_instance = member_functions.get(f_name)

        res[f_name]['code'] = source_code_to_html(f_instance)
        if f_name == 'get_recession_start_or_end':
            sub_res = ''
        else:
            sub_res = f_instance(ins)
            if isinstance(sub_res, pd.DataFrame):
                sub_res = sub_res.head(50).to_html().rstrip('\r\n')
            else:
                if f_name == 'run_ttest':
                    sub_res = (str(sub_res[0]), sub_res[1], sub_res[2])
                sub_res = f'<p>{sub_res}</p>'

        res[f_name]['result'] = sub_res

    return json.dumps(res)
