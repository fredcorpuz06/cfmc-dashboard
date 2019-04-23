import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

from app import app, indicator, grants, funds
from app_utils import graphers
colors = {"background": "#F3F6FA", "background_div": "white"}

YEARS = grants.year.unique().astype(int)
REGIONS = grants.region.unique()
IMPACTS = grants.project_impact.unique()
NONPROFIT_NAMES = grants.org_name.unique()
PAGE_SIZE = 15

# Utils
pg = graphers.PlotlyGrapher()

# Data 
top_controls = [
    
    html.Div(
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
        style={'width': '90%', 'padding': '0px 20px 20px 20px', 'display': 'inline-block'}
    ),

    html.Div(
        dcc.Checklist(
            id='regionChoices1',
            options=[{'label': r, 'value': r} for r in REGIONS],
            values=[REGIONS[0], REGIONS[1]]
        ),
        style={'width': '25%', 'float': 'left'}
    ),

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

indicators = [
    indicator(
        "No. of Grants",
        "nGrants"
    ),
    indicator(
        "Most Impacted Region",
        "grantsAwarded"
    ),
    indicator(
        "Most Impacted Project Area",
        "grantRegion"
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
grantN_bar = [
    html.Div([
        html.P('No. of grants received'),
        dcc.Graph(
            id='grantsNPie',
            config=dict(displayModeBar=False),
            style={'height': '89%', 'width': '98%'}
        ),
    ], 
    className='six columns chart_div'),

    html.Div([
        html.P('Project Impacts'),
        dcc.Graph(
            id='impactsNPie',
            config=dict(displayModeBar=False),
            style={'height': '89%', 'width': '98%'}
        ),
    ], 
    className='six columns chart_div')

]

layout = [
    html.Div(top_controls, className="row"),
    html.Div(indicators, className='row'),
    html.Div(grantN_bar, className='row'),
    html.Div(orgs_table),
    html.Div(id='intermediate-value', style={'display': 'none'})
]


@app.callback(
    [
        Output("nGrants", "children"), 
        Output("grantsAwarded", "children"), 
        Output("grantRegion", "children"), 
    ],
    [
        Input('intermediate-value', 'children'),
    ]
)
def nFunds_callback(json_dff):
    dff = pd.read_json(json_dff, orient='split')
    n_grants = dff.shape[0]
    most_region = dff.region.mode().tolist()[0]
    most_impact = dff.project_impact.mode().tolist()[0]

    return n_grants, most_region, most_impact

@app.callback(
    Output('orgsTable', 'data'),
    [
        Input('intermediate-value', 'children'),
        Input('orgsTable', 'pagination_settings')
    ]
)
def orgsTable_callback(json_dff, page_s):
    dff = pd.read_json(json_dff, orient='split')
    startP = page_s['current_page'] * page_s['page_size']
    endP = (page_s['current_page'] + 1) * page_s['page_size']

    dff = dff.iloc[startP:endP]

    return dff.to_dict('rows')

@app.callback(
    Output('grantsNPie', 'figure'),
    [
        Input('intermediate-value', 'children'),
    ]
)
def grantsNPie_callback(json_dff):
    dff = pd.read_json(json_dff, orient='split')
    g = dff[['region', 'program_name']].groupby('region')
    rez = g.agg(lambda x: np.shape(x)[0])['program_name']
    slices = [{
        'name': 'Regions',
        'label': rez.index.tolist(),
        'value': rez.tolist(),
    }]
    return pg.pie_chart(slices)

@app.callback(
    Output('impactsNPie', 'figure'),
    [
        Input('intermediate-value', 'children'),
    ]
)
def impactsNPie_callback(json_dff):
    dff = pd.read_json(json_dff, orient='split')
    g = dff[['project_impact', 'program_name']].groupby('project_impact')
    rez = g.agg(lambda x: np.shape(x)[0])['program_name']
    slices = [{
        'name': 'Project Impact',
        'label': rez.index.tolist(),
        'value': rez.tolist(),
    }]
    return pg.pie_chart(slices)


@app.callback(
    Output('intermediate-value', 'children'),
    [
        Input('nonprofitName1', 'value'),
        Input('nonProfitAll1', 'on'),
        Input('yearRange1', 'value'),
        Input('regionChoices1', 'values'),
        Input('impactChoices1', 'values')
    ]
)
def orgsTable_callback(names, allNps, yearRange, regions, impacts):
    dff = grants
    dff = dff[(dff.year >= yearRange[0]) & (dff.year <= yearRange[1])]
    if len(regions) > 1:
        pat = '|'.join(regions)
    else:
        pat = regions[0]
    dff = dff[dff.region.str.contains(pat, regex=True)]

    if len(impacts) > 1:
        pat = '|'.join(impacts)
    else:
        pat = impacts[0]
    dff = dff[dff.project_impact.str.contains(pat, regex=True)]

    if len(names) > 1:
        pat = '|'.join(names)
    else:
        pat = names[0]
    # turn on the nonprofit selector
    if allNps:
        dff = dff[dff.org_name.str.contains(pat, regex=True)]

    return dff.to_json(date_format='iso', orient='split')