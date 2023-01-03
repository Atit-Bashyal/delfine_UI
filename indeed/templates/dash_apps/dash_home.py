# import dash
# from dash import dcc
# from dash import html
# #from django_plotly_dash import DjangoDash
# from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc
#
# import pandas as pd
# import plotly.express as px
#
# app = DjangoDash('home')
#
# external_stylesheets = [dbc.themes.BOOTSTRAP]
#
# app.css.append_css({
#     "external_url": external_stylesheets
# })
#
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
#
# graph = html.Div([
#         dcc.Graph(id='graph-with-slider'),
#         dcc.Slider(
#             id='year-slider',
#             min=df['year'].min(),
#             max=df['year'].max(),
#             value=df['year'].min(),
#             marks={str(year): str(year) for year in df['year'].unique()},
#             step=None
#         )
#     ])
#
# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         dbc.NavItem(dbc.NavLink("Page 2", href="#")),
#         dbc.NavItem(dbc.NavLink("Page 3", href="#")),
#         # dbc.DropdownMenu(
#         #     children=[
#         #         dbc.DropdownMenuItem("More pages", header=True),
#         #         dbc.DropdownMenuItem("Page 2", href="#"),
#         #         dbc.DropdownMenuItem("Page 3", href="#"),
#         #     ],
#         #     nav=True,
#         #     in_navbar=True,
#         #     label="More",
#         # ),
#     ],
#     brand="INDEED",
#     brand_href="#",
#     color="primary",
#     dark=True,
# )
#
# app.layout = html.Div([
#     navbar,
#     graph,
# ])
#
# @app.callback(
#     Output('graph-with-slider', 'figure'),
#     Input('year-slider', 'value'))
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#
#     fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
#                      size="pop", color="continent", hover_name="country",
#                      log_x=True, size_max=55)
#
#     fig.update_layout(transition_duration=500)
#
#     return fig
