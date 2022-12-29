import pandas as pd
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
from django.conf import settings
from django_plotly_dash import DjangoDash
import urllib.parse

import sys
sys.path.insert(0, f'{settings.BASE_DIR}/utils')
from dataset import loadData
from api import getAPI

# Initialize the app
external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('Simpletable', external_stylesheets=external_css)

data = loadData()
data.loadDataFromDir(dirPath=f"{settings.BASE_DIR}/data/")



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
                    "padding-bottom": "30px",
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
            dcc.Location(id='api_href', refresh=False),
            html.Div(
                style={
                    "display": "grid",
                    "grid-template-columns": "30fr 68fr 2fr",
                    # "padding": "10px",
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
                    dcc.Clipboard(
                        target_id="api_forecast",
                        title="copy",
                        style={
                            "display": "inline-block",
                            "fontSize": 20,
                            "verticalAlign": "center",
                            "horizontalAlign": "middle",
                        },
                    ),
                ]
            ),
            html.Div(
                style={
                    "display": "grid",
                    "grid-template-columns": "50fr 50fr",
                    # "padding": "10px",
                },
                children=[
                    html.Label(
                        ["Table:"],
                        style={
                            "font-weight": "bold",
                            "text-align": "left",
                        }
                    ),
                    # To select showing rows
                    dcc.Dropdown(
                        id='table_row', 
                        options=list(range(5,101,5)),
                        value=5,
                        clearable=False,
                        searchable=False,
                        # className='div-for-dropdown',
                        style={
                            "display": "flex",
                            "justify-self": "end",
                        },
                    ),
                ]
            ),
            dash_table.DataTable(
                id="table_show",
                style_table={
                    'overflowX': 'auto',
                    'minWidth': '100%',
                    },
                style_cell={
                    'textAlign': 'center',
                    'height': 'auto',
                    'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',
                    'whiteSpace': 'normal',},
            ),
        ]
    )
)


# Callback for timeseries price
@app.callback(
    [Output('api_forecast', 'children'),
     Output('table_show', 'data'),],
    [Input("api_typeSelecter", "value"),
     Input("api_planSelecter", "value"),
     Input("api_locSelecter", "value"),
     Input("api_dateSelecter", "date"),
     Input('api_href', 'href'),
     Input("table_row", "value"),],
)
def process(
    api_type,
    api_plan,
    api_loc,
    api_date,
    api_href,
    table_row,
    
    ):
    parse_url = urllib.parse.urlparse(api_href)
    api_hostname = f"{parse_url.scheme}://{parse_url.netloc}"
    # api_hostname = "http://localhost:8000"

    ####################
    # Pseudo code for table
    ## 1. Get data from the selected api. -> api_data
    ##  E.g. for api result should be
    ##  [{'datetime': Timestamp('2019-02-14 09:15:00'), 'power': 0.678},
    ##   {'datetime': Timestamp('2019-02-14 09:30:00'), 'power': 0.78},
    ##   {'datetime': Timestamp('2019-02-14 09:45:00'), 'power': 0.912},
    ##   {'datetime': Timestamp('2019-02-14 10:00:00'), 'power': 1.025},
    ##   {'datetime': Timestamp('2019-02-14 10:15:00'), 'power': 1.126}]
    ## 2. Put it to pandas DataFrame -> df = pd.DataFrame(api_data)
    ## 3. Select a number of row from the top -> df = df.head(table_row)
    ## 4. Styling data
    ##  4.1 Specify decimal places -> df = df.round(4)
    ## 5. Convert to dict('record') -> api_table = df.to_dict('records')
    ## E.g.
    api_data = data.dataAll["Mehring-power"].reset_index(level=0)
    df = api_data
    df = df.head(table_row)
    df = df.round(decimals=4)
    api_table = df.to_dict('records')
    ####################

    return [getAPI(api_hostname, api_type, api_plan, api_loc, api_date), api_table]

if __name__ == '__main__':
    app.run_server(debug=True)