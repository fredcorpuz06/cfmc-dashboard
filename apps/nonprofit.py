import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

from app import app, indicator, grants, funds
from app_utils import graphers
colors = {"background": "#F3F6FA", "background_div": "white"}


NONPROFIT_NAMES = grants.org_name.unique()
PAGE_SIZE = 15

# Utils
pg = graphers.PlotlyGrapher()

# Data 
top_controls = [
    html.Div(
        dcc.Dropdown(
            id='nonprofitName',
            options=[{'label': s, 'value': s} for s in NONPROFIT_NAMES],
            value=NONPROFIT_NAMES[0],
            clearable=False,
        ),
        className='two columns'
    )
]

indicators = [
    indicator(
        "#00cc96",
        "No. of Grants Received",
        "nGrants"
    ),
    indicator(
        "#00cc96",
        "% Awarded $/Requested $",
        "percGranted"
    ),
    indicator(
        "#00cc96",
        "Most Impacted Area",
        "nRegion"
    ),
]

orgs_table = [
    html.Div([
        html.P('All grants of selected organization'),
        dash_table.DataTable(
            id='orgsTable',
            columns=[{"name": i, "id": i} for i in grants.columns],
            pagination_settings={
                'current_page': 0,
                'page_size': PAGE_SIZE
            },
            pagination_mode='be',
            style_data={'whiteSpace': 'normal'},
            css=[{
                'selector': '.dash-cell div.dash-cell-value',
                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
            }],
        )
    ])
]
# Graphs

layout = [
    html.Div(top_controls, className="row"),
    html.Div(indicators, className='row'),
    html.Div(orgs_table),
]

@app.callback(
    Output("nGrants", "children"), 
    [
        Input('nonprofitName', 'value')
    ]
)
def nGrants_callback(name):
    dff = grants
    dff = dff[dff.org_name == name]
    return dff.shape[0]

@app.callback(
    Output("percGranted", "children"), 
    [
        Input('nonprofitName', 'value')
    ]
)
def percGranted_callback(name):
    dff = grants
    dff = dff[dff.org_name == name]
    requested = dff.requested_damt.sum()
    granted = dff.grant_damt.sum()
    return "{0:.2f}%".format(granted*100/requested)

@app.callback(
    Output("nRegion", "children"), 
    [
        Input('nonprofitName', 'value')
    ]
)
def nRegion_callback(name):
    dff = grants
    dff = dff[dff.org_name == name]
    
    return dff.project_impact.mode()







@app.callback(
    Output('orgsTable', 'data'),
    [
        Input('orgsTable', 'pagination_settings'),
        Input('nonprofitName', 'value')
    ]
)
def orgsTable_callback(page_s, name):
    dff = grants
    dff = dff[dff.org_name == name]
    startP = page_s['current_page'] * page_s['page_size']
    endP = (page_s['current_page'] + 1) * page_s['page_size']

    dff = dff.iloc[startP:endP]

    return dff.to_dict('rows')
