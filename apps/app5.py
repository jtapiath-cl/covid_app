import dash
import dash_table

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dash_table import Format as dtf
from dash.dependencies import Input, Output

from app import app
from src import setup_etl as st

data_tbl, comunas, regiones = st.data_etl()

layout = []