import pandas as pd

from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
from dash.dependencies import Input, Output
from django.conf import settings
from django_plotly_dash import DjangoDash

data_path = str(settings.BASE_DIR) + '/data/merkel1.csv'
# Load data
df = pd.read_csv(data_path, index_col=0, parse_dates=True)
df = df.sort_index()

# Initialize the app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('Simpletimeseries', external_stylesheets=external_stylesheets)


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div(
    children=[
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='four columns div-user-controls',
                    children=[
                        html.H2('DASH - STOCK PRICES'),
                        html.P('Visualising time series with Plotly - Dash.'),
                        html.P('Pick one or more stocks from the dropdown belo.'),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='stockselector', options=get_options(df['Power'].unique()),
                                            multi=True, value=[df['Power'].sort_values()[0]],
                                            style={'backgroundColor': '#1E1E1E'},
                                            className='stockselector'
                                            ),
                            ],
                            style={'color': '#1E1E1E'}
                        )
                    ]
                ),
            #     html.Div(
            #         className='eight columns div-for-charts bg-grey',
            #         children=[
            #             # dcc.Graph(id='timeseries', config={'displayModeBar': False}, animate=True)
            #             # dcc.Graph(
            #             #     id="Main-Graph",
            #             #     figure={
            #             #         "layout": {
            #             #             "margin": {
            #             #                 "t": 30, "r": 35, "b": 40, "l": 50},
            #             #             "xaxis": {
            #             #                 "dtick": 5,
            #             #                 "gridcolor": "#636363",
            #             #                 "showline": False},
            #             #             "yaxis": {
            #             #                 "showgrid": False, 
            #             #                 "showline": False},
            #             #             "plot_bgcolor": "black",
            #             #             "paper_bgcolor": "black",
            #             #             "font": {
            #             #                 "color": "gray"},
            #             #         },
            #             #     },
            #             #     config={"displayModeBar": False},
            #             # ),
            #             # html.Pre(id="update-on-click-data"),
            #         ]
            #     )
            ]
        )
    ]
)

"""
# Callback for timeseries price
@app.callback(
    Output('timeseries', 'figure'),
    [Input('stockselector', 'value')]
)
def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(
            x=df_sub[df_sub['stock'] == stock].index,
            y=df_sub[df_sub['stock'] == stock]['value'],
            mode='lines',
            opacity=0.7,
            name=stock,
            textposition='bottom center')
        )
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {
        'data': data,
        'layout': go.Layout(
            colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
            template='plotly_dark',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            margin={'b': 15},
            hovermode='x',
            autosize=True,
            title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
            xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
        ),
    }

    return figure
"""