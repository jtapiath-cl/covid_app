# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, 
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions = True,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}] 
                )

app.title = "COVID-19 en Chile"

server = app.server