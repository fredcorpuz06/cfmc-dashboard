import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import os
import psycopg2


from app import app, indicator
from app_utils import graphers, data_managers
colors = {"background": "#F3F6FA", "background_div": "white"}



# Data 
grants = pd.read_csv("./data/grants_clean.csv")
funds = pd.read_csv("./data/funds_clean.csv")
# DATABASE_URL = os.environ['DATABASE_URL']
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# grants = pd.read_sql_query("SELECT * FROM grants;", conn)
# funds = pd.read_sql_query("SELECT * FROM funds;", conn)


YEARS = grants.year.unique().astype(int)
SUMMARY_TYPES = ['gross_total', 'count', 'ave_amt']
# var_choices = ['fund_type', 'project_impact', 'org_impact', 'region']
VAR_CHOICES = ['project_impact', 'org_impact', 'region']

PAGE_SIZE = 15


# Utils
pg = graphers.PlotlyGrapher()
dm = data_managers.DataMunger(SUMMARY_TYPES)


# General functions
def global_subset(yearRange, varChoice1, varChoice2):
    '''Filter to years in range and select variables of interest.'''
    if varChoice1 == 'fund_type':
        df = funds
    else:
        df = grants

    dff = df[(df.year >= yearRange[0]) & (df.year <= yearRange[1])]
    dff = dff[[varChoice1, varChoice2, 'grant_damt']]

    return dff

# Graphs

    
layout = [
    # top controls
    html.Div(
        [
            html.Div(
                dcc.RangeSlider(
                    id='yearRange',
                    min=YEARS.min(),
                    max=YEARS.max(),
                    marks={y: str(y) for y in YEARS},
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
                    value=VAR_CHOICES[1],
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
        ],
        className="row",
        style={},
    ),
    # first row graphs
    html.Div(
        [
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
        ],
        className='row',
        style={'marginTop': '5px'}
    ),

    # second row graphs
    html.Div(
        [
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
        ],
        className='row',
        style={'marginTop': '5px'}
    ),

    # data table
    html.Div(
        [
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
                    filtering='be',
                    filtering_settings='',
                    sorting='be',
                    sorting_type='multi',
                    sorting_settings=[],

                    style_data={'whiteSpace': 'normal'},
                    css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],
                )
           ]) 
        ]
    )

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
    df = funds
    dff = df[(df.year >= yearRange[0]) & (df.year <= yearRange[1])]
    # if varChoice1 == varChoice2:
    dff = dff[['fund_type', varChoice1, varChoice2, 'fund_damt']]

    # dff = dm.getYearVars(funds, yearRange, varChoice1, varChoice2)
    g = dff.groupby(['fund_type', varChoice1, varChoice2])
    rez = g.agg([np.sum, lambda x: np.shape(x)[0], np.mean]).rename(columns={
        'sum': SUMMARY_TYPES[0],
        '<lambda>': SUMMARY_TYPES[1],
        'mean': SUMMARY_TYPES[2]
    })['fund_damt'].reset_index()

    rez01 = rez[['fund_type', varChoice1] + SUMMARY_TYPES].rename(columns={
        'fund_type': 'source',
        varChoice1: 'target'
    })
    rez01['target'] = rez01.target + '0'

    rez12 = rez[[varChoice1, varChoice2] + SUMMARY_TYPES].rename(columns={
        varChoice1: 'source',
        varChoice2: 'target'
    })
    rez12['source'] = rez12.source + '0'
    
    rez_all = rez01.append(rez12, ignore_index=True)
    

    source_nodes = rez_all.source.tolist()
    target_nodes = rez_all.target.tolist()
    all_nodes = set(source_nodes + target_nodes)

    myMap = {}
    for i, n in enumerate(sorted(all_nodes)):
        myMap[n] = i

    rez_all = rez_all.replace(myMap)
    # print(rez_all)

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
    dff = dm.getYearVars(funds, yearRange, varChoice1)
    rez = dm.create_summaries(dff, 'grant_damt', [varChoice1])
    
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
    dff = dm.getYearVars(funds, yearRange, varChoice1, 'year')
    rez = dm.create_summaries(dff, 'grant_damt', [varChoice1, 'year'])

    print(rez)
    times = []
    for name, group in rez.groupby(level=0):
        bar = {
            'name': name,
            'label': [i[1] for i in group.index],
            'value': group[summaryType].tolist(),
        }
        times.append(bar)
    print(times)

    return pg.time_line(times)



@app.callback(
    Output('grantsTable', 'data'),
    [
        Input('grantsTable', 'pagination_settings'),
        Input('grantsTable', 'sorting_settings'),
        Input('grantsTable', 'filtering_settings'),
    ]
)

def grantsTable_callback(page_s, sort_s, filter_s):
    filter_exps = filter_s.split(' && ')
    dff = grants
    for f in filter_exps:
        if ' eq ' in f:
            col_name = f.split(' eq ')[0]
            filter_value = f.split(' eq ')[1]
            dff = dff.loc[dff[col_name] == filter_value]
        elif ' > ' in f:
            col_name = f.split(' > ')[0]
            filter_value = f.split(' > ')[1]
            dff = dff.loc[dff[col_name] > filter_value]
        elif ' < ' in f:
            col_name = f.split(' < ')[0]
            filter_value = f.split(' < ')[1]
            dff = dff.loc[dff[col_name] < filter_value]
    
    if len(sort_s):
        dff = dff.sort_values(
            by=[col['column_id'] for col in sort_s],
            ascending=[col['direction'] == 'asc' for col in sort_s],
            inplace=False
        )

    startP = page_s['current_page'] * page_s['page_size']
    endP = (page_s['current_page'] + 1) * page_s['page_size']

    return dff.iloc[startP:endP].to_dict('rows')

