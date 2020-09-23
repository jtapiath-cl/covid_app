import dash

import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from app import app
from analisis import post_1_magallanes as contenido_1

parrafo = """
La intención de esta sección es entregar una mirada rápida respecto de la efectividad
de las políticas públicas que se han definido en Chile para manejar la pandemia, desde
la perspectiva de las técnicas del análisis y la ciencia de datos.  
_Notas del editor_: Esta sección está optimizada para ser vista en dispositivos de alta resolución,
como tablets y computadores. Verla en un celular entregará una experiencia incompleta."""
footer = "_Fuente: [Ministerio de Ciencia, Tecnología, Conocimiento e Innovación](https://github.com/MinCiencia/Datos-COVID19)_"

## ===
contenido_analisis = """En esta sección, puedes elegir los distintos análisis que se han realizados de
los datos de la pandemia. Los botones muestran la región analizada y la fecha del análisis."""
contenido_inicial = """Elige uno de los distintos análisis que se han realizado respecto de los
datos de la pandemia."""
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
                        dcc.Markdown(children = parrafo, id = "page-desc"),
                        html.Br(),
                        dbc.ButtonGroup(
                            [
                                dbc.Button("Inicio", id = "post-0"),
                                dbc.Button("Magallanes: 23/Sep", id = "post-1")
                            ],
                            size = "lg",
                            className = "mr-1"
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            id = "fila-3-grafico",
            children = 
                [
                    dbc.Jumbotron(
                        children = [
                            dbc.Row(
                                dbc.Col(id = "columna-2-contenido",
                                            children = 
                                            [
                                                html.Div(id = "contenido-analisis", 
                                                            children = contenido_analisis),
                                            ]
                                )
                            )
                        ],
                        style = {"background-color": "transparent"}
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

@app.callback(
    Output("contenido-analisis", "children"),
    [
        Input("post-0", "n_clicks"),
        Input("post-1", "n_clicks")
    ]
)
def mostrar_analisis(boton_inicio, post_1):
    ctx = dash.callback_context

    if not ctx.triggered:
        return contenido_inicial
    else:
        button_pressed = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_pressed == "post-0":
            return contenido_analisis
        elif button_pressed == "post-1":
            return contenido_1.layout
        else:
            return "404"