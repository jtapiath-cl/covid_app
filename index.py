import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from src import setup as stp
stp.main_function()

from app import app
from apps import app1, app2, sidebar

# the styles for the main content position it to the right of the sidebar and
# add some padding.
HEADER_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding-top": "2rem",
    "padding-left": "1rem",
    "padding-bottom": "0.5rem"
}

CONTENT_STYLE = {
    "position": "relative",
    "margin-left": "18rem",
    "margin-right": "2rem"
}

header_item = html.Div(id="header", style = HEADER_STYLE, children = [html.H1(children = "COVID-19 en Chile: un análisis")])

content = html.Div(id="page-content", style = CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id = "url"), header_item, sidebar.sidebar_layout, content])

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

if __name__ == "__main__":
    app.run_server(debug = False, host = "0.0.0.0", port = 8050,
                    dev_tools_hot_reload = True)