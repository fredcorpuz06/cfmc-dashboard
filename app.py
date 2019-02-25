# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

impact_money = pd.read_csv("./data/impact_total_money.csv")
fund_yearly_money = pd.read_csv("./data/fund_yearly_money.csv")

my_years = fund_yearly_money['year'].unique().astype(int)
fund_types = fund_yearly_money['Fdescript'].unique()
money_metrics = ['total_DAmt', 'count', 'avg_DAmt']

app.layout = html.Div([
    html.H1('CFMC Dashboard', style={'width': '49%'}),
    # html.Img(src='./img/cfmc.png', alt='CFMC Logo'),

    html.Div('''
        This dashboard is for the use of the Board of Directors of the 
        Community Foundation of Middlesex County. Trends in the incoming 
        funds and the outgoing grants will be analyzed with the 
        interactive visualizations on this dashboard. Eventually, a 
        community-facing version will be constructed. 
    ''',
    style={'width': '49%'}),

    html.Div([
        dcc.Dropdown(
            id='crossfilter-fund-source',
            options=[{'label': i, 'value': i} for i in fund_types],
            value='Donor Advised'
        ),
    ],
    style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.RadioItems(
            id='crossfilter-money-metric',
            options=[{'label': i, 'value':i} for i in money_metrics],
            value='total_DAmt'
        )
    ],
    style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Slider(
            id='crossfilter-year-slider',
            min=my_years.min(),
            max=my_years.max(),
            value=my_years.max(),
            marks={str(year): str(year) for year in my_years}
        )
    ],
    style={'width': '90%', 'padding': '0px 20px 20px 20px', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(id='bar-money-impact'),
        dcc.Graph(id='bar-fund-yearly-money'),
    ],
    style={'width': '98%', 'padding': '0px 20px 20px 20px', 'columnCount': 2}),    

   
])

@app.callback(
    Output('bar-money-impact', 'figure'),
    [
        Input('crossfilter-fund-source', 'value'),
        Input('crossfilter-money-metric', 'value'),
        Input('crossfilter-year-slider', 'value')
    ]
)
def update_bar_fund(fund_source, money_metric, year):
    dff = impact_money[['year', 'impact_area', 'Fdescript', money_metric]]
    dff = dff[(dff.Fdescript == fund_source) & (dff.year == year)]
    # print(dff)

    return {
        'data':[go.Bar(
            x=dff.impact_area,
            y=dff.iloc[:, 3]
        )],
        'layout': {
            'title': '{} by Impact Area from {} in {}'.format(money_metric, fund_source, year)
        }
    }

@app.callback(
    Output('bar-fund-yearly-money', 'figure'),
    [
        Input('crossfilter-money-metric', 'value'),
        Input('crossfilter-year-slider', 'value')
    ]   
)
def update_bar_yearly(money_metric, year):
    dff = fund_yearly_money[['year', 'Fdescript', money_metric]]
    dff = dff[dff.year == year]
    # print(dff)

    return {
        'data': [go.Bar(
            x=dff.Fdescript,
            y=dff.iloc[:, 2],
            
        )],
        'layout': {
            'title': '{} by Fund Type in {}'.format(money_metric, year)
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
    # , dev_tools_hot_reload=False