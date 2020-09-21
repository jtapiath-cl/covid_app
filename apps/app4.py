import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from analisis import post_1_magallanes as contenido

parrafo = """
La intención de esta sección es entregar una mirada rápida respecto de la efectividad
de las políticas públicas que se han definido en Chile para manejar la pandemia, desde
la perspectiva de las técnicas del análisis y la ciencia de datos."""
footer = "_Fuente: [Ministerio de Ciencia, Tecnología, Conocimiento e Innovación](https://github.com/MinCiencia/Datos-COVID19)_"

## ===
contenido_analisis = contenido.layout
## ===

layout = dbc.Container(
    children = 
    [
        dbc.Row(
            id = "fila-1-intro",
            children = [
                dbc.Col(
                    id = "intro-comentarios",
                    children = [
                        html.H2(children = "Análisis de políticas públicas"),
                        html.P(children = parrafo, id = "page-desc")
                    ]
                )
            ]
        ),
        dbc.Row(
            id = "fila-3-grafico",
            children = 
                [
                    dbc.Col(id = "columna-2-contenido",
                                children = 
                                [
                                    html.Br(),
                                    html.Div(id = "contenido-analisis", 
                                                children = contenido_analisis),
                                    html.Br()
                                ]
                    )
                ]
        ),
        dbc.Row(
            id = "fila-4-footer",
            children = [
                dbc.Col(
                    id = "columna-1-footer",
                    children = [dcc.Markdown(children = footer)]
                )
            ]
        )
    ]
)