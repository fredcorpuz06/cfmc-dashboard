# print('Summaries')

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import os
import psycopg2

from app import app, indicator

colors = {"background": "#F3F6FA", "background_div": "white"}

# Data 
# grants = pd.read_csv("./data/grants_clean.csv")
# funds = pd.read_csv("./data/funds_clean.csv")
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
grants = pd.read_sql_query("SELECT * FROM grants;", conn)
funds = pd.read_sql_query("SELECT * FROM funds;", conn)

df = grants

years = grants.year.unique().astype(int)
summary_types = ['gross_total', 'count', 'ave_amt']
var_choices = ['fund_type', 'project_impact', 'org_impact', 'region']
PAGE_SIZE = 15

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
def time_line(time_values, mode='lines+markers'):
    traces = [go.Scatter(
        x=t['label'],
        y=t['value'],
        name=t['name'],
        mode=mode,
    ) for t in time_values]

    layout = go.Layout(
        margin=dict(l=40, r=25, b=40, t=0, pad=4)
    )
    return {'data': traces, 'layout': layout}

def pie_chart():
    # traces = [go.Pie(label=s['labels'], values=s['values']) for s in slices]

    trace = go.Pie(
        labels=['a','b'],
        values=[1,2],
        # markers={'colors': ["#264e86", "#74dbef"]}
    )
    traces = [trace]

    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=4, pad=8),
        legend=dict(orientation="h"),
    )

    return {'data': traces, 'layout': layout}

def bar_chart(bars, barmode='stack'):

    traces = [go.Bar(
        x=b['label'], y=b['value'], name=b['name']
    ) for b in bars]
    # data = [t for t in traces]
    layout = go.Layout(
        barmode=barmode,
        margin=dict(l=40, r=25, b=40, t=0, pad=4),
    )

    return {'data': traces, 'layout': layout}

def histogram(hists, barmode='overlay'):
    traces = [go.Histogram(x=h['values'], opacity=0.75) for h in hists]   
    layout = go.Layout(
        barmode=barmode,
        margin=dict(l=40, r=25, b=40, t=0, pad=4),
    )
    return {'data': traces, 'layout': layout}


def sankey_diag(flows):
    # flows = pd.read_csv('./data/scratch.csv')
    # flows = pd.read_csv('./data/scratch3.csv')
    for k, f in flows.items()   :
        # print(f.unique())
        print(k, len(f))
    node=dict(
        pad=15,
        thickness=20,
        line=dict(
            color='black',
            width=0.5
        ),
        
        # label=flows.label[:14],
        # label=flows.label[:14],
        label=flows['label'],
        # color=["blue", "blue", "blue", "blue", "blue", "blue"]
    )
    link=dict(
        # source=flows.source,
        # target=flows.target,
        # value=flows.value,
        source=flows['source'],
        target=flows['target'],
        value=flows['value'],
        
    )    
    trace = go.Sankey(node=node, link=link)
    
    layout = go.Layout(
        margin=dict(l=40, r=25, b=40, t=40, pad=4),
    )
    
    # dcc.Graph(figure={'data': [data_trace], 'layout': layout})
    return {'data': [trace], 'layout': layout}

    
layout = [
    # top controls
    html.Div(
        [
            html.Div(
                dcc.RangeSlider(
                    id='yearRange',
                    min=years.min(),
                    max=years.max(),
                    marks={i: str(i) for i in years},
                    step=1,
                    # value=[years.min(), years.max()]
                    value=[2008, 2015]
                ),
                style={'width': '90%', 'padding': '0px 20px 20px 20px', 'display': 'inline-block'}
            ),


            # html.Div(
            #     dcc.Slider(
            #         id="yearRange",
            #         marks={str(i): str(i) for i in years},
            #         min=years.min(),
            #         max=years.max(),
            #         value=years.max()
            #     ),
            #     className="two columns",

            #     # style={"marginBottom": "10"},
            #     style={'width': '90%', 'padding': '0px 20px 20px 20px', 'display': 'inline-block'}

            # ),
            
            html.Div(
                dcc.Dropdown(
                    id="summaryType",
                    options=[
                        {"label": summary_types[0], "value": summary_types[0]},
                        {"label": summary_types[1], "value": summary_types[1]},
                        {"label": summary_types[2], "value": summary_types[2]},
                    ],
                    value=summary_types[0],
                    clearable=False,
                ),
                className="two columns",
            ),
            html.Div(
                dcc.Dropdown(
                    id="varChoice1",
                    options=[
                        {"label": var_choices[0], "value": var_choices[0]},
                        {"label": var_choices[1], "value": var_choices[1]},
                        {"label": var_choices[2], "value": var_choices[2]},
                        {"label": var_choices[3], "value": var_choices[3]},
                    ],
                    value=var_choices[1],
                    clearable=False,
                ),
                className="two columns",
            ),
            html.Div(
                dcc.Dropdown(
                    id="varChoice2",
                    options=[
                        {"label": var_choices[0], "value": var_choices[0]},
                        {"label": var_choices[1], "value": var_choices[1]},
                        {"label": var_choices[2], "value": var_choices[2]},
                        {"label": var_choices[3], "value": var_choices[3]},
                    ],
                    value=var_choices[3],
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
    # indicators 
    html.Div(
        [
            indicator(
                "#00cc96",
                "Low priority cases",
                "left_cases_indicator",
            ),
            indicator(
                "#119DFF",
                "Medium priority cases",
                "middle_cases_indicator",
            ),
            indicator(
                "#EF553B",
                "High priority cases",
                "right_cases_indicator",
            ),
        ],
        className="row",
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

            # html.Div([
            #     html.P('Breakdown of'),
            #     dcc.Graph(
            #         id='singleVarPie',
            #         config=dict(displayModeBar=False),
            #         style={'height': '89%', 'width': '98%'}
            #     ),
            # ],
            # className="six columns chart_div"),        
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
                    id='singleVarBar',
                    config=dict(displayModeBar=False),
                    style={'height': '89%', 'width': '98%'}
                ),
            ],
            className="six columns chart_div"), 

            html.Div([
                html.P('Breakdown over time'),
                dcc.Graph(
                    id='singleVarHist',
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
                    columns=[{"name": i, "id": i} for i in df.columns],
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

# indicator interactions
@app.callback(
    Output("left_cases_indicator", "children"),
    [
        Input('varChoice1', 'value'),
    ]
)
def left_cases_indicator_callback(df):
    return 1


@app.callback(
    Output("middle_cases_indicator", "children"), 
    [
        Input('varChoice1', 'value'),
    ]
)
def middle_cases_indicator_callback(df):
    return 2


@app.callback(
    Output("right_cases_indicator", "children"), 
    [
        Input('varChoice1', 'value'),

    ]
)
def right_cases_indicator_callback(df):
    return 3

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
def graph1_callback(yearRange, summaryType, varChoice1, varChoice2):
    
    df = funds
    dff = df[(df.year >= yearRange[0]) & (df.year <= yearRange[1])]
    dff = dff[['fund_type', varChoice1, varChoice2, 'fund_damt']]

    g = dff.groupby(['fund_type', varChoice1, varChoice2])
    rez = g.agg([np.sum, lambda x: np.shape(x)[0], np.mean]).rename(columns={
        'sum': summary_types[0],
        '<lambda>': summary_types[1],
        'mean': summary_types[2]
    })['fund_damt'].reset_index()

    rez01 = rez[['fund_type', varChoice1] + summary_types].rename(columns={
        'fund_type': 'source',
        varChoice1: 'target'
    }
    )
    rez12 = rez[[varChoice1, varChoice2] + summary_types].rename(columns={
        varChoice1: 'source',
        varChoice2: 'target'
    })

    rez_all = rez01.append(rez12, ignore_index=True)
    # rez_all = rez01
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

    return sankey_diag(flows)

@app.callback(
    Output('singleVarPie', 'figure'),
    [
        Input('varChoice1', 'value'),
        Input('summaryType', 'value'),
    ]
)
def graph2_callback(c1, c2):
    return pie_chart()

@app.callback(
    Output('singleVarBar', 'figure'),
    [
        Input('yearRange', 'value'),
        Input('summaryType', 'value'),
        Input('varChoice1', 'value'),
        Input('varChoice2', 'value')
    ]
)
def singleVarBar_callback(yearRange, summaryType, varChoice1, varChoice2):
    # doesn't allow for same varChoice, and not doing funds properly
    if varChoice1 == 'fund_type':
        df = funds
    else:
        df = grants

    dff = df[(df.year >= yearRange[0]) & (df.year <= yearRange[1])]
    dff = dff[[varChoice1, varChoice2, 'grant_damt']]

    # Summarize by 1
    
    g = dff.groupby(varChoice1)
    
    rez = g.agg([np.sum, lambda x: np.shape(x)[0]], np.mean).rename(columns={
                'sum': summary_types[0],
                '<lambda>': summary_types[1],
                'mean': summary_types[2],
            })['grant_damt']
    # print(rez)
    # Format data for bar graph
    bars =[{
        'name': varChoice1,
        'label': rez.index.tolist(),
        'value': rez[summaryType].tolist()
    }]           
    
    # print(bars)
    return bar_chart(bars)

@app.callback(
    Output('singleVarHist', 'figure'),
    [
        Input('yearRange', 'value'),
        Input('summaryType', 'value'),
        Input('varChoice1', 'value'),
    ]
)
def graph4_callback(yearRange, summaryType, varChoice1):
    if varChoice1 == 'fund_type':
        df = funds
    else:
        df = grants

    dff = df[(df.year >= yearRange[0]) & (df.year <= yearRange[1])]
    dff = dff[['year', varChoice1, 'grant_damt']]

    g = dff.groupby([varChoice1, 'year'])
    rez = g.agg([np.sum, lambda x: np.shape(x)[0], np.mean]).rename(columns={
            'sum': summary_types[0],
            '<lambda>': summary_types[1],
            'mean': summary_types[2],
        })['grant_damt']

    times = []
    for name, group in rez.groupby(level=0):
        bar = {
            'name': name,
            'label': [i[1] for i in group.index],
            'value': group[summaryType].tolist(),
        }
        times.append(bar)


    return time_line(times)



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
    dff = df
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


print('Summaries finish execution')
