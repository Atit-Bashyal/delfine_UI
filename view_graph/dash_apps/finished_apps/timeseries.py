import sys
sys.path.insert(0, '/Users/kritkorns/Mike/Jacob/x_others/03_delfine_Django/delfine_UI/utils')

from dataset import loadData

from dash import html
from dash import dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
from django.conf import settings
from django_plotly_dash import DjangoDash
import datetime as dt


# Initialize the app
external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('Simpletimeseries', external_stylesheets=external_css)

data = loadData()
data.loadDataFromDir(dirPath=f"{settings.BASE_DIR}/data/")
data.dataAll['merkel1-Power'].loc[dt.date(2019, 3, 1):dt.date(2019, 3, 31)]

app.layout = html.Div(
    style={
        "hight": "100%",
    },
    children=[
        html.H2('Delfine - Data Charts'),
        html.P('Visualising data with time series plot. Please select from the dropdowns below.'),
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='four columns div-user-controls',
                    style={
                        "width": "68%",
                        "display": "inline-block",
                        "color": "black",
                    },
                    children=[
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(
                                    id='dataSelecter', 
                                    options=data.getDataKeys(),
                                    multi=True, 
                                    value=[data.getDataKeys()[0]],
                                    # style={'backgroundColor': '#1E1E1E'},
                                    className='stockselector'
                                ),
                            ],
                        )
                    ],
                ),
                html.Div(
                    style={
                        # "vertical-align": "top",
                        # "position": "absolute",
                        "width": "30%",
                        "right": "3%",
                        "float": "right",
                        "display": "inline-block",
                    },
                    children=[
                        dcc.DatePickerRange(
                            id="dateSelecter",
                            start_date=data.datemin,
                            end_date=data.datemax,
                            min_date_allowed=data.datemin,
                            max_date_allowed=data.datemax,
                            initial_visible_month=data.datemin,
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            calendar_orientation="horizontal",
                            # calendar_orientation="vertical",
                        ),
                        # html.Div(id="output-container-date-picker-range"),
                    ],
                ),
            ]
        ),        
        html.Div(
            # className='eight columns div-for-charts bg-grey',
            style={
                "width": "95%",
                "display": "inline-block"
            },
            children=[
                dcc.Graph(
                    id="timeseries",
                    config={"displayModeBar": False},
                    animate=True,
                ),
            ],
        ),
    ]
)

# Callback for timeseries price
@app.callback(
    [Output('timeseries', 'figure'),],
    [Input("dataSelecter", "value"),
     Input("dateSelecter", "start_date"),
     Input("dateSelecter", "end_date"),],
)
def process(
    dataNames,
    startDate, 
    endDate,
    ):

    graphs = []
    for dataName in dataNames:
        graphs.append(go.Scatter(
            mode='lines',
            x=data.dataAll[dataName].loc[startDate:endDate].index,
            y=data.dataAll[dataName].loc[startDate:endDate],
            opacity=0.7,
            name=dataName,
            textposition='bottom center'))

    fig = go.Figure(data=graphs)
    fig.update_layout(
        go.Layout(
            xaxis=dict(
                range=[startDate, endDate],
            ),
            hovermode='x unified',
            # hovermode='x',
        )
    )
    return [fig]

if __name__ == '__main__':
    app.run_server(debug=True)