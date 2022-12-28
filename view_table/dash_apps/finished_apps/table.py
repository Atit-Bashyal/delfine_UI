import sys
sys.path.insert(0, '/Users/kritkorns/Mike/Jacob/x_others/03_delfine_Django/delfine_UI/utils')

from dataset import loadData
from api import getAPI

from dash import html
from dash import dcc
from dash import Dash, dash_table
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
from django.conf import settings
from django_plotly_dash import DjangoDash
import datetime as dt
import pathlib
# from utils.delfine_dataset import loadData

# Initialize the app
external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('Simpletable', external_stylesheets=external_css)
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = loadData()
data.loadDataFromDir(dirPath=f"{settings.BASE_DIR}/data/")
# print(data.dataAll['merkel1-Power'].loc[dt.date(2019, 3, 1):dt.date(2019, 3, 31)])
print(dict(data.dataAll["Mehring-power"].head()))

app.layout = html.Div(
    html.Div(
        className='row', 
        children=[
            html.H2('Delfine - Data Table'),
            html.P('Visualising data with time series plot. Please select from the dropdowns below.'),
            html.Div(
                style={
                    "display": "grid",
                    "grid-template-columns": "50fr 50fr",
                    "padding": "10px",
                },
                children=[
                    html.Div(
                        style={
                            "display": "grid",
                            "grid-template-columns": "30fr 70fr",
                            "width": "50%",
                        },
                        children=[
                            html.Label(
                                ["Type:"], 
                                style={
                                    "font-weight": "bold",
                                    "text-align": "left",
                                },
                            ),
                            dcc.Dropdown(
                                id='api_typeSelecter', 
                                options=["wind", "solar"],
                                placeholder="Select a type",
                                # className='div-for-dropdown',
                            ),
                        ]
                    ),
                    html.Div(
                        style={
                            "display": "grid",
                            "grid-template-columns": "30fr 70fr",
                            "width": "50%",
                        },
                        children=[
                            html.Label(
                                ["Plan:"], 
                                style={
                                    "font-weight": "bold",
                                    "text-align": "left",
                                },
                            ),
                            dcc.Dropdown(
                                id='api_planSelecter', 
                                options=["short_term", "long_term"],
                                placeholder="Select a plan",
                                # className='div-for-dropdown',
                            ),
                        ]
                    ),
                    html.Div(
                        style={
                            "display": "grid",
                            "grid-template-columns": "30fr 70fr",
                            "width": "50%",
                        },
                        children=[
                            html.Label(
                                ["Location:"], 
                                style={
                                    "font-weight": "bold",
                                    "text-align": "left",
                                },
                            ),
                            dcc.Dropdown(
                                id='api_locSelecter', 
                                options=["location1", "location2", "location3"],  # Need to change to city name
                                placeholder="Select a location",
                                # className='div-for-dropdown',
                            ),
                        ]
                    ),
                    html.Div(
                        style={
                            "display": "grid",
                            "grid-template-columns": "30fr 70fr",
                            "width": "50%",
                        },
                        children=[
                            html.Label(
                                ["Date:"], 
                                style={
                                    "font-weight": "bold",
                                    "text-align": "left",
                                },
                            ),
                            dcc.DatePickerSingle(
                                id='api_dateSelecter', 
                                min_date_allowed=data.datemin,
                                max_date_allowed=data.datemax,
                                initial_visible_month=data.datemin,
                                calendar_orientation="horizontal",
                                style={
                                    "float": "right",
                                    "display": "inline-block"
                                }
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(
                style={
                    "display": "grid",
                    "grid-template-columns": "30fr 70fr",
                    "padding": "10px",
                },
                children=[
                    html.Label(
                        ["API:"],
                        style={
                            "font-weight": "bold",
                            "text-align": "left",
                        }
                    ),
                    html.Label(
                        id="api_forecast",
                        style={
                            "text-align": "left",
                        },
                    ),
                ]
            ),
            # dash_table.DataTable(
            #     data=dict(data.dataAll["Mehring-power"].head()),
            #     columns=["power"],
            #     # [{"name": i, "id": i} for i in df.columns]
            # )
        ]
    )
)

# Callback for timeseries price
@app.callback(
    [Output('api_forecast', 'children'),],
    [Input("api_typeSelecter", "value"),
     Input("api_planSelecter", "value"),
     Input("api_locSelecter", "value"),
     Input("api_dateSelecter", "date"),],
)
def process(
    api_type,
    api_plan,
    api_loc,
    api_date
    ):

    return [getAPI("http://localhost:8000", api_type, api_plan, api_loc, api_date)]

if __name__ == '__main__':
    app.run_server(debug=True)