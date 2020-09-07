# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

def update_data():
    from src import setup as stp
    from src import setup_env as se
    from src import setup_git as sg
    from src import setup_data as sd
    from src import setup_etl as st
    from src import helpers
    stp.main_function()
    return None

app = dash.Dash(__name__)

csv_loc = os.path.join(os.getenv("BASE_APP_PATH"), "data", "data.csv")
df = pd.read_csv(csv_loc)

fig = px.line(df, x = "fecha", y = "casos", color = "comuna", line_group = "region")

app.layout = html.Div(children=[
    html.H1(children = "Hello Dash"),
    html.Div(children = """
        Dash: A web application framework for Python.
    """),

    dcc.Graph(
        id = "example-graph",
        figure  =fig
    )
])

if __name__ == "__main__":
    # app.run_server(debug = True, host = "0.0.0.0", port = 8050)
    update_data()
    app.run_server(debug = False, host = "0.0.0.0", port = 8050)