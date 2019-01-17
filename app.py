""" 
    Flask app serving csv data using pandas.
    Graphs mobile data coverage for selected area.

    Author: Vaughn de Villiers
    Email: vaughndevilliers@gmail.com
    Date: 17 January 2019

    prerequisite: python version 3.7+
                  pip

    Setup in terminal:
        pip install -r requirements.txt
        export SECRET_KEY="your-own-very-sercert-key"
        export WTF_CSRF_SECRET_KEY="your-own-very-sercert-csrf-key"
    
    Running on default port 5000 from terminal:
        python app.py
    
    Navigate browser to:
        http://127.0.0.1:5000/
"""

from flask import url_for
from flask import request
from flask import render_template
from flask import redirect
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
import pandas as pd
import os

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY= os.environ['SECRET_KEY'],
    WTF_CSRF_SECRET_KEY= os.environ['WTF_CSRF_SECRET_KEY']
))


""" Reads the given csv file into a pandas dataframe
    and then selects the columns that will be used
"""
df = pd.read_csv('2016_mobile_ctyua_r01.csv')
df = df[['la_code', 
         'la_name', 
         '4G premises (outdoor): signal from all operators by LA (%)', 
         '4G premises (indoor): signal from all operators by LA (%)',
         '4G geographic (outdoor): signal from all operators by LA (%)', 
         '4G geographic (indoor): signal from all operators by LA (%)', 
         '4G roads: signal from all operators by LA (%)',
         '3G premises (outdoor): signal from all operators by LA (%)',
         '3G premises (indoor): signal from all operators by LA (%)',
         '3G geographic (outdoor): signal from all operators by LA (%)',
         '3G geographic (indoor): signal from all operators by LA (%)',
         '3G roads: signal from all operators by LA (%)',
         '2G premises (outdoor): signal from all operators by LA (%)',
         '2G premises (indoor): signal from all operators by LA (%)',
         '2G geographic (outdoor): signal from all operators by LA (%)',
         '2G geographic (indoor): signal from all operators by LA (%)',
         '2G roads: signal from all operators by LA (%)',
        ]]


""" locations is a list of tuple pairs that is 
    used in the choices in the select input box
"""
locations = list(zip(df['la_code'].tolist(), df['la_name'].tolist()))


class DataForm(FlaskForm):
    """ 
    """
    locations = SelectField(u'locations', 
                            choices = locations, 
                            validators = [DataRequired()]
                            )


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Serves landing page: http://127.0.0.1:5000/
    """
    form = DataForm()
    if form.validate_on_submit():
        location = form.locations.data
        
        return redirect(url_for('chart', location=location))
    return render_template('index.html', form=form)


@app.route('/chart')
def chart(chartID='chart_ID', chart_type='bar', chart_height=350):
    """ Serves chart for specified location: 
        Example:    http://127.0.0.1:5000/chart?location=00-QA
    """
    loc = request.args['location']
    df1 = df.copy()                                     # Prevent changes to original dataframe in this instance
    df1 = df1.loc[df['la_code'] == loc]                 # Restricts dataframe to requested row
    cols = list(df1)[2:]                                # Creates list from column names
    cols = [x.split(':', 1)[0] for x in cols]           # Shortens column names
    vals = df1.values.tolist()                          # Creates list of values for the requested row
    area = '{} ({})'.format(vals[0][1], vals[0][0])     # Creates sting of area name for labling the graph
    vals = [float(x.strip('%')) for x in vals[0][2:]]   # Converts the string percentages to float values

    """ Setup varibles passed to the template 
        and used in the displayed graph
    """
    series = [{"name": 'Signal from all operators by LA (%)', "data": vals}]
    title = {"text": area}
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    xAxis = {"categories": cols}
    yAxis = {"title": {"text": 'Coverage Percentage'}}

    return render_template('chart.html', chartID=chartID, chart=chart, 
                            series=series, title=title, xAxis=xAxis, yAxis=yAxis)


if __name__ == '__main__':
    app.run()


