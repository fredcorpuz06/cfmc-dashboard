import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app, server
from apps import overview, nonprofit, fund, reference



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
                        dcc.Tab(label='Funds & Grants Overview', value='overview_tab'),
                        dcc.Tab(label='Funds at a Glance', value='funds_tab'),
                        dcc.Tab(label='Nonprofits at a Glance', value='nonprofits_tab'),
                        # dcc.Tab(label='Reference Tables', value='references_tab'),

                    ],
                    value='overview_tab',
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
    if tab == 'overview_tab':
        return overview.layout
    elif tab == 'nonprofits_tab':
        return nonprofit.layout
    elif tab == 'funds_tab':
        return fund.layout
    elif tab == 'references_tab':
        return reference.layout

if __name__ == '__main__':
    app.run_server(debug=True)