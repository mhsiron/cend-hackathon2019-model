from flask import Flask, render_template, request

import plotly.graph_objs as go
import datetime

import pandas as pd

#main_data = pd.read_pickle("./static/data-with-dates-converted.pickle")
print(main_data.columns)

def create_plot(filter=None):

    ## fake data:
    from scipy.stats import norm
    import numpy as np

    x = np.arange(-4, 4, 0.001)
    y = norm.pdf(x)

    if filter:
        pass

    fig = go.Figure(data=go.Scatter(x=x, y=y))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="New Infections",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )

    #graphJSON = json.dumps(fig.to_json(), cls=plotly.utils.PlotlyJSONEncoder)

    return fig.to_json()

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def index():
    map = create_plot()

    fields = [
        ("agg-emergency", "State of Emergency"),
        ("agg-travel", "Travel Restriction"),
        ("agg-quarantine", "Quarantine"),
        ("agg-health", "Health Checks"),
        ("agg-healthcare", "Accessibility to Healthcare"),
        ("agg-business", "Non-Essential Business Closure"),
        ("agg-distance", "Social Distancing"),
        ("agg-transit", "Public Transit Closing"),
        ("agg-mapping", "Contact Mapping"),
        ("agg-sanitation", "Sanitation"),
        ("agg-resources", "Easing Resource Shortage"),
        ("agg-education", "Increase Public Education"),
        ("agg-humanitarian", "Humanitarian Relief"),
    ]

    if request.method == "POST":
        filter = pd.Timestamp(request.form.get("date"))
        date = filter
        map, data = create_plot(filter)

    return render_template('index.html', title="Welcome", plot=map, fields=fields,
                           table=None,date=datetime.date.today(), cases=None)
@app.route('/date', methods=['GET', 'POST'])
def change_features():

    filter = request.args['datefield']
    graphJSON= create_plot(pd.Timestamp(filter))[0]

    return graphJSON

@app.route('/<int:year>/<int:month>/<int:day>/')
def load_from_date_filter(year,month,day):
    date = pd.Timestamp(year,month,day)
    map, data = create_plot(date)

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
                           table=reduced_data, date=date)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',)
