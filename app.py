# -*- coding: utf-8 -*-
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import psycopg2


server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server
)
app.config.suppress_callback_exceptions = True


try:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    grants = pd.read_sql_query("SELECT * FROM grants;", conn)
    funds = pd.read_sql_query("SELECT * FROM funds;", conn)
except KeyError:
    print('*'*20)
    print('IN PRODUCTION MODE')
    print('*'*20)
    grants = pd.read_csv("./data/grants_clean.csv")
    funds = pd.read_csv("./data/funds_clean.csv")




#returns top indicator div
def indicator(color, text, id_value):
    return html.Div(
        [
            
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
        
    )