import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

from app import app, indicator, grants, funds
from app_utils import graphers, data_managers
colors = {"background": "#F3F6FA", "background_div": "white"}


YEARS = grants.year.unique().astype(int)
SUMMARY_TYPES = ['gross_total', 'count', 'ave_amt']
VAR_CHOICES = ['project_impact', 'org_impact', 'region']

PAGE_SIZE = 15


# Utils
pg = graphers.PlotlyGrapher()
dm = data_managers.DataMunger(SUMMARY_TYPES)


# 
top_controls = [
    html.Div(
        dcc.RangeSlider(
            id='yearRange',
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
        dcc.Dropdown(
            id="summaryType",
            options=[{'label': s, 'value': s} for s in SUMMARY_TYPES],
            value=SUMMARY_TYPES[0],
            clearable=False,
        ),
        className="two columns",
    ),
    html.Div(
        dcc.Dropdown(
            id="varChoice1",
            options=[{'label': v, 'value': v} for v in VAR_CHOICES],
            value=VAR_CHOICES[0],
            clearable=False,
        ),
        className="two columns",
    ),
    html.Div(
        dcc.Dropdown(
            id="varChoice2",
            options=[{'label': v, 'value': v} for v in VAR_CHOICES],
            value=VAR_CHOICES[2],
            clearable=False,
        ),
        className="two columns",
    ),

    # add button
    html.Div(
        html.Span(
            "Add new",
            id="button1",
            n_clicks=0,
            className="button button--primary add",
            
        ),
        className="two columns",
        style={"float": "right"},
    ),
]

sankey = [
    html.Div([
        html.P('Flow of funds to projects'),
        dcc.Graph(
            id='sankey',
            config=dict(displayModeBar=False),
            style={'height': '89%', 'width': '98%'}
        ),
    ],
    className="twelve columns chart_div",
    style={"height": 700}),    
]

bar_and_line = [
    html.Div([
        html.P('Breakdown overall'),
        dcc.Graph(
            id='overallBar',
            config=dict(displayModeBar=False),
            style={'height': '89%', 'width': '98%'}
        ),
    ],
    className="six columns chart_div"), 

    html.Div([
        html.P('Breakdown over time'),
        dcc.Graph(
            id='overallTime',
            config=dict(displayModeBar=False),
            style={'height': '89%', 'width': '98%'}
        ),
    ],
    className="six columns chart_div"),         
]

data_table = [
    html.Div([
        html.P('Top 5 grant recepients'),
        dash_table.DataTable(
            id='grantsTable',
            columns=[{"name": i, "id": i} for i in grants.columns],
            pagination_settings={
                'current_page': 0,
                'page_size': PAGE_SIZE
            },
            pagination_mode='be',
            # filtering='be',
            # filtering_settings='',
            # sorting='be',
            # sorting_type='multi',
            # sorting_settings=[],

            style_data={'whiteSpace': 'normal'},
            css=[{
                'selector': '.dash-cell div.dash-cell-value',
                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
            }],
        )
    ]) 
]


layout = [
    # top controls
    html.Div(top_controls, className="row", style={}),
    # first row graphs
    html.Div(sankey, className='row', style={'marginTop': '5px'}),
    # second row graphs
    html.Div(bar_and_line, className='row', style={'marginTop': '5px'}),
    # data table
    html.Div(data_table),

]

# graph interactions
@app.callback(
    Output('sankey', 'figure'),
    [
        Input('yearRange', 'value'),
        Input('summaryType', 'value'),
        Input('varChoice1', 'value'),
        Input('varChoice2', 'value')
    ]
)
def sankey_callback(yearRange, summaryType, varChoice1, varChoice2):
    myVar = 'fund_damt'
    if varChoice1 == varChoice2:
        aggVars = ['fund_type', varChoice1]
    else: 
        aggVars = ['fund_type', varChoice1, varChoice2]
    
    dff = dm.get_year_vars(funds, yearRange, myVar, aggVars)      
    rez = dm.create_summaries(dff, myVar, aggVars).reset_index()
    rez_all, myMap = dm.sankey_manipulations(rez, aggVars)

    flows = {
        'source': rez_all.source.tolist(),
        'target': rez_all.target.tolist(),
        'value': rez_all[summaryType].tolist(),
        'label': list(sorted(myMap.keys())),

    }

    return pg.sankey_diag(flows)

@app.callback(
    Output('overallBar', 'figure'),
    [
        Input('yearRange', 'value'),
        Input('summaryType', 'value'),
        Input('varChoice1', 'value'),
    ]
)
def overallBar_callback(yearRange, summaryType, varChoice1):
    myVar = 'grant_damt'
    aggVars = [varChoice1]
    dff = dm.get_year_vars(grants, yearRange, myVar, aggVars) 
    rez = dm.create_summaries(dff, myVar, aggVars)
    # Format data for bar graph
    bars =[{
        'name': varChoice1,
        'label': rez.index.tolist(),
        'value': rez[summaryType].tolist()
    }]           
    
    return pg.bar_chart(bars)

@app.callback(
    Output('overallTime', 'figure'),
    [
        Input('yearRange', 'value'),
        Input('summaryType', 'value'),
        Input('varChoice1', 'value'),
    ]
)
def overallTime_callback(yearRange, summaryType, varChoice1):
    myVar = 'grant_damt'
    aggVars = [varChoice1, 'year']
    dff = dm.get_year_vars(grants, yearRange, myVar, aggVars) 
    rez = dm.create_summaries(dff, myVar, aggVars)

    times = []
    for name, group in rez.groupby(level=0):
        bar = {
            'name': name,
            'label': [i[1] for i in group.index],
            'value': group[summaryType].tolist(),
        }
        times.append(bar)

    return pg.time_line(times)



@app.callback(
    Output('grantsTable', 'data'),
    [
        Input('grantsTable', 'pagination_settings'),
        # Input('grantsTable', 'sorting_settings'),
        # Input('grantsTable', 'filtering_settings'),
    ]
)

# def grantsTable_callback(page_s, sort_s, filter_s):
def grantsTable_callback(page_s):
    dff = grants
    
    # filter_exps = filter_s.split(' && ')
    # for f in filter_exps:
    #     if ' eq ' in f:
    #         col_name = f.split(' eq ')[0]
    #         filter_value = f.split(' eq ')[1]
    #         dff = dff.loc[dff[col_name] == filter_value]
    #     elif ' > ' in f:
    #         col_name = f.split(' > ')[0]
    #         filter_value = f.split(' > ')[1]
    #         dff = dff.loc[dff[col_name] > filter_value]
    #     elif ' < ' in f:
    #         col_name = f.split(' < ')[0]
    #         filter_value = f.split(' < ')[1]
    #         dff = dff.loc[dff[col_name] < filter_value]
    
    # if len(sort_s):
    #     dff = dff.sort_values(
    #         by=[col['column_id'] for col in sort_s],
    #         ascending=[col['direction'] == 'asc' for col in sort_s],
    #         inplace=False
    #     ) 

    startP = page_s['current_page'] * page_s['page_size']
    endP = (page_s['current_page'] + 1) * page_s['page_size']

    dff = dff.iloc[startP:endP]

    return dff.to_dict('rows')

