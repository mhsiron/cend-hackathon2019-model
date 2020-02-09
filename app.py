from flask import Flask, render_template


import plotly
import plotly.graph_objs as go
import datetime

import pandas as pd
import numpy as np
import json

main_data = pd.read_pickle("./static/data-with-dates-converted.pickle")
print(main_data.columns)

def create_plot(filter=None):
    data_limited = main_data[main_data["new_case_highest-N-text_extract"].notnull()]

    fig = go.Figure(
        go.Densitymapbox(lat=data_limited["lat"], lon=data_limited["lon"],
                         z=data_limited["new_case_highest-N-text_extract"],
                         radius=40, ))
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, mapbox=dict(
        bearing=0,
        center=dict(  # Looks like only this parameter is now used
            lat=32,  # el inicio!
            lon=112
        ),
        pitch=0,
        zoom=3,
    ), )

    #graphJSON = json.dumps(fig.to_json(), cls=plotly.utils.PlotlyJSONEncoder)

    return fig.to_json(),data_limited

app = Flask(__name__)


@app.route('/')
def index():
    map,data= create_plot()
    columns = ['Source', 'descriptions', 'titles', 'dates',
               'locations_identified_titles','latlon_titles',
               'new_case_highest-N-text_extract',
               'acc_case_highest-N-text_extract',
               'locations_identified_descriptions',
               'acc_case_highest-N-prob',
               'new_case_highest-N-prob',
               'acc_case_highest-I-text',
               'new_case_highest-I-text']
    reduced_data = data[columns]
    return render_template('index.html', title="Welcome", plot=map,
                           table=reduced_data,date=datetime.date(2020,1,27))

@app.route('/<year>/<month>/<day>/')
def load_from_date_filter(year,month,day):
    map, data = create_plot(datetime.date(year,month,day))

    columns = ['Source', 'descriptions', 'titles', 'dates',
               'locations_identified_titles', 'latlon_titles',
               'new_case_highest-N-text_extract',
               'acc_case_highest-N-text_extract',
               'locations_identified_descriptions',
               'acc_case_highest-N-prob',
               'new_case_highest-N-prob',
               'acc_case_highest-I-text',
               'new_case_highest-I-text']
    reduced_data = data[columns]

    return render_template('index.html', title="Welcome", plot=map,
                           table=reduced_data, date=datetime.date(2020, 1, 27))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',)
