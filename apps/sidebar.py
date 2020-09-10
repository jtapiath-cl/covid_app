import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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

sidebar_layout = html.Div(
    [
        html.H3("Navbar", className="display-16"),
        html.Hr(),
        html.P(
            "Secciones", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Tabla de datos", href = "/page-1", id = "page-1-link"),
                dbc.NavLink("Totales comparativos", href = "/page-2", id = "page-2-link"),
                dbc.NavLink("Incrementales comparativos", href = "/page-3", id = "page-3-link"),
                dbc.NavLink("Comentarios", href = "/page-4", id = "page-4-link")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)