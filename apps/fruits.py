from dash import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import psycopg2
import os

# DATABASE_URL = os.environ['DATABASE_URL']
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# cur = conn.cursor()
# cur.execute("SELECT region FROM funds")
# fund_region = cur.fetchall()
# cur.execute("SELECT region FROM grants")
# grant_region =cur.fetchall()

# print(fund_region)
# print(grant_region)

from app import app

layout = html.Div(children=[
    html.H1(
        children='Hello Dash'
    ),

    html.Div(
        children='''Dash: A web application framework for Python.'''
    ),

    dcc.Graph(
        id='example-graph',
       figure=go.Figure(
            data=[
                go.Bar(
                # x=fruits1, y=sales1, name='SF'),
                x=[1, 2, 3], y=[2, 4, 5], name='SF')
            ],

            #'layout':{
            #    'title': 'Dash Data Visualization'
            #}
        )
    )
])
