import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app, server
# from apps import summaries, trends, fruits
from apps import trends, fruits


app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Span('CFMC Dashboard', className='app-title'),
                html.Div(
                    html.Img(
                        src='https://middlesexcountycf.org/wp-content/uploads/2015/09/image_logo.png',
                        height="100%"),
                    style={"float":"right","height":"100%"}
                ),
            ],
            className="row header"
        ),

        # tabs
        html.Div(
            [
                dcc.Tabs(
                    id='tabs',
                    style={'height':'20', 'verticalAlign':'middle'},
                    children=[
                        dcc.Tab(label='Time Period Summaries', value='summaries_tab'),
                        dcc.Tab(label='Time Trends', value='trends_tab'),
                        dcc.Tab(label='Fruits Sample', value='fruits_tab'),

                    ],
                    value='fruits_tab',
                )
            ], 
            className='row tabs_div'
        ),

        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),

        
    ],
    className="row",
    style={"margin": "0%"},
)


@app.callback(
    Output('tab_content', 'children'),
    [
        Input('tabs', 'value')
    ]
)
def render_content(tab):
    if tab == 'summaries_tab':
        return fruits.layout
    elif tab == 'trends_tab':
        return trends.layout
    elif tab == 'fruits_tab':
        return fruits.layout
    else:
        return fruits.layout


if __name__ == '__main__':
    app.run_server(debug=True)
    # , dev_tools_hot_reload=False