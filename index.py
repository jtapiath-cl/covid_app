import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from src import setup_env as se
se.set_environment()

import os
environment = "production"
os.environ["FLASK_ENV"] = environment

from app import app
from apps import app1, app2, app3, sidebar

content = html.Div(
            id="page-content"
            )

app.layout = html.Div(
                [
                    dcc.Location(id = "url"),
                    sidebar.sidebar_layout, 
                    content
                ]
            )

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname in ["/", "/page-1"]:
        return app1.layout
    elif pathname == "/page-2":
        return app2.layout
    else:
        return "404"

@app.callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run_server(debug = True, 
        host = "0.0.0.0", 
        port = 8050,
        dev_tools_hot_reload = False
        )
