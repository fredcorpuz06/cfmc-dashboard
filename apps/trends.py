# print('Time trends')

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app, indicator

colors = {"background": "#F3F6FA", "background_div": "white"}

# Data 

# Graphs
def time_line():
    trace = go.Bar(
        x=[1,2], y=[1,2]
    )
    data = [trace]
    layout = go.Layout(
        barmode="stack",
        margin=dict(l=40, r=25, b=40, t=0, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {'data': data, 'layout': layout}

def pie_chart():
    trace = go.Pie(
        labels=['a','b'],
        values=[1,2],
        # markers={'colors': ["#264e86", "#74dbef"]}
    )
    data = [trace]
    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=4, pad=8),
        legend=dict(orientation="h"),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    return {'data': data, 'layout': layout}

layout = [
    # top controls
    html.Div(
        [
            html.Div(
                dcc.Dropdown(
                    id="control1b",
                    options=[
                        {"label": "By day", "value": "D"},
                        {"label": "By week", "value": "W-MON"},
                        {"label": "By month", "value": "M"},
                    ],
                    value="D",
                    clearable=False,
                ),
                className="two columns",
                style={"marginBottom": "10"},
            ),
            html.Div(
                dcc.Dropdown(
                    id="control2b",
                    options=[
                        {"label": "All priority", "value": "all_p"},
                        {"label": "High priority", "value": "High"},
                        {"label": "Medium priority", "value": "Medium"},
                        {"label": "Low priority", "value": "Low"},
                    ],
                    value="all_p",
                    clearable=False,
                ),
                className="two columns",
            ),
            html.Div(
                dcc.Dropdown(
                    id="control3b",
                    options=[
                        {"label": "All origins", "value": "all"},
                        {"label": "Phone", "value": "Phone"},
                        {"label": "Web", "value": "Web"},
                        {"label": "Email", "value": "Email"},
                    ],
                    value="all",
                    clearable=False,
                ),
                className="two columns",
            ),

            # add button
            html.Div(
                html.Span(
                    "Add new",
                    id="button1b",
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
                "left_cases_indicator2",
            ),
            indicator(
                "#119DFF",
                "Medium priority cases",
                "middle_cases_indicator2",
            ),
            indicator(
                "#EF553B",
                "High priority cases",
                "right_cases_indicator2",
            ),
        ],
        className="row",
    ),

    # first row graphs
    html.Div(
        [
            html.Div([
                html.P('Graph 1'),
                dcc.Graph(
                    id='graph1b',
                    config=dict(displayModeBar=False),
                    style={'height': '89%', 'width': '98%'}
                ),
            ],
            className="six columns chart_div"), 

            html.Div([
                html.P('Graph 2'),
                dcc.Graph(
                    id='graph2b',
                    config=dict(displayModeBar=False),
                    style={'height': '89%', 'width': '98%'}
                ),
            ],
            className="six columns chart_div"),         
        ],
        className='row',
        style={'marginTop': '5px'}
    ),

    # second row graphs
    html.Div(
        [
            html.Div([
                html.P('Graph 3'),
                dcc.Graph(
                    id='graph3b',
                    config=dict(displayModeBar=False),
                    style={'height': '89%', 'width': '98%'}
                ),
            ],
            className="six columns chart_div"), 

            html.Div([
                html.P('Graph 4'),
                dcc.Graph(
                    id='graph4b',
                    config=dict(displayModeBar=False),
                    style={'height': '89%', 'width': '98%'}
                ),
            ],
            className="six columns chart_div"),         
        ],
        className='row',
        style={'marginTop': '5px'}
    ),

]

# indicator interactions
@app.callback(
    Output("left_cases_indicator2", "children"),
    [
        Input("control1b", "children")
    ]
)
def left_cases_indicator2_callback(df):
    return 1


@app.callback(
    Output("middle_cases_indicator2", "children"), 
    [
        Input("control1b", "value")
    ]
)
def middle_cases_indicator2_callback(df):
    return 2


@app.callback(
    Output("right_cases_indicator2", "children"), 
    [
        Input("control1b", "value")
    ]
)
def right_cases_indicator2_callback(df):
    return 3


# interactions
@app.callback(
    Output('graph1b', 'figure'),
    [
        Input('control1b', 'value'),
        Input('control2b', 'value')
    ]
)
def graph1b_callback(c1, c2):
    return pie_chart()

@app.callback(
    Output('graph2b', 'figure'),
    [
        Input('control1b', 'value'),
        Input('control2b', 'value')
    ]
)
def graph2b_callback(c1, c2):
    return pie_chart()

@app.callback(
    Output('graph3b', 'figure'),
    [
        Input('control1b', 'value'),
        Input('control2b', 'value')
    ]
)
def graph3_callback(c1, c2):
    return time_line()

@app.callback(
    Output('graph4b', 'figure'),
    [
        Input('control1b', 'value'),
        Input('control2b', 'value')
    ]
)
def graph4_callback(c1, c2):
    return time_line()


print('Trends finish execution')