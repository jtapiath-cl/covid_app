import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("COVID", className="display-4")),
        dbc.Col(
            html.Button(
                html.Span(className="navbar-toggler-icon"),
                className="navbar-toggler",
                # the navbar-toggler classes don't set color, so we do it here
                style={
                    "color": "rgba(0,0,0,.5)",
                    "border-color": "rgba(0,0,0,.1)",
                },
                id="toggle",
            ),
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar_layout = html.Div(
    [
        sidebar_header,
        html.Div(
            [
                html.Br(),
                html.P("Un análisis de la evolución de la pandemia",
                        className = "lead")
            ],
            id = "blurb"
        ),
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Gráfico comparativo", href = "/page-1", id = "page-1-link"),
                    dbc.NavLink("Tabla de datos", href = "/page-2", id = "page-2-link"),
                    dbc.NavLink("Incrementos", href = "/page-3", id = "page-3-link"),
                    dbc.NavLink("Análisis", href = "/page-4", id = "page-4-link")
                ],
                vertical=True,
                pills=True,
            ),
            id = "collapse"
        )
    ],
    id = "sidebar"
)