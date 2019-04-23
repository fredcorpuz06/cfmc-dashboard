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


layout = [
   html.H1(children='Hello world')
]