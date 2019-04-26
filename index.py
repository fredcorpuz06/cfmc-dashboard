import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from app import app, indicator, grants, funds
from app_utils import graphers, data_managers


YEARS = grants.year.unique().astype(int)
REGIONS = grants.region.unique()
IMPACTS = grants.project_impact.unique()
NONPROFIT_NAMES = grants.org_name.unique()
PAGE_SIZE = 15

# Utils
pg = graphers.PlotlyGrapher()


top_controls = [
    

    dcc.RangeSlider(
        id='yearRange1',
        min=YEARS.min(),
        max=YEARS.max(),
#         marks={y: str(y) for y in YEARS},
        marks= {
            1997: '1997', 1998: '1998', 1999: '1999', 
            2000: '2000', 2001: '2001', 2002: '2002', 
            2003: '2003', 2004: '2004', 2005: '2005', 
            2006: '2006', 2007: '2007', 2008: '2008', 
            2009: '2009', 2010: '2010', 2011: '2011', 
            2012: '2012', 2013: '2013', 2014: '2014', 
            2015: '2015', 2016: '2016', 2017: '2017', 
            2018: '2018'
        },
        step=1,
        value=[YEARS.min(), YEARS.max()]
    ),

    html.Div(
        dcc.Checklist(
            id='regionChoices1',
            options=[{'label': r, 'value': r} for r in REGIONS],
            values=[REGIONS[0], REGIONS[1]]
        ),
        style={'width': '25%', 'float': 'left'}
    ),

]

top_controls2 = [
    html.Div(
        dcc.Checklist(
            id='impactChoices1',
            options=[{'label': r, 'value': r} for r in IMPACTS],
            values=[IMPACTS[0], IMPACTS[1]]
        ),
        style={'width': '25%', 'float': 'left'}
    ),
    

    html.Div([
        dcc.Dropdown(
            id='nonprofitName1',
            options=[{'label': s, 'value': s} for s in NONPROFIT_NAMES],
            value=[NONPROFIT_NAMES[0],NONPROFIT_NAMES[1]],
            multi=True,
        ),
        daq.BooleanSwitch(
            id='nonProfitAll1',
            on=False
        ),
    ], style={'width': '50%', 'float': 'right'})

]


app.layout = html.Div([
    # header
    html.Div([
        html.H2('CFMC Dashboard', id='title'),
        html.Img(
            src='https://middlesexcountycf.org/wp-content/uploads/2015/09/image_logo.png',
        ),
    ],
        className='banner'
    ),


    # Tab content
    html.Div(top_controls,
        className='container'
    ),

    # Tab content 2
    html.Div(top_controls2,
        className='container'
    )
])



if __name__ == '__main__':
    app.run_server(debug=True)