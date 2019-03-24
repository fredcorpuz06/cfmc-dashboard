from dash import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import psycopg2
import os
import pandas as pd

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
# cur.execute("SELECT region FROM funds")
# fund_region = cur.fetchall()
# cur.execute("SELECT region FROM grants")
# grant_region =cur.fetchall()

# print(fund_region)
# print(grant_region)

cur.execute('SELECT label FROM forluck;')
label = cur.fetchall()
label = [l[0] for l in label]
cur.execute('SELECT value FROM forluck;')
value = cur.fetchall()
value = [v[0] for v in value]

print('Without pandas:', label, value)
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
forluck = pd.read_sql_query("SELECT * FROM forluck;", conn)
print('With pandas:', forluck.label, forluck.value)

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
                x=forluck.label, y=forluck.value, name='SF'),
                # x=[1, 2, 3], y=[2, 4, 5], name='SF')
            ],

            #'layout':{
            #    'title': 'Dash Data Visualization'
            #}
        )
    )
])
