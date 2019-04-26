import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output

from app import app, indicator, grants, funds
from app_utils import graphers, data_managers


YEARS = grants.year.unique().astype(int)
SUMMARY_TYPES = ['gross_total', 'count', 'ave_amt']
VAR_CHOICES = ['project_impact', 'org_impact', 'region']

PAGE_SIZE = 15


# Utils
pg = graphers.PlotlyGrapher()
dm = data_managers.DataMunger(SUMMARY_TYPES)

layout = []