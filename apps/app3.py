import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

import pandas as pd
from src import setup_etl as st

def generar_grafico(df: pd.DataFrame, regiones: bool = False, comunas: bool = False,
                    region_flt = None, comunas_flt = None):
    error = False
    # Logica del grafico
    if not regiones and not comunas:
        ## Grafico del total
        groupbys = ["fecha"]
        title_txt = "Casos a nivel nacional"
        str_hover_1 = "<span style='font-size:16px'><b>Total nacional</b></span><br><br>"
        str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
        color_default = None
        custom_default = None
        data_tmp = df
    elif regiones and not comunas:
        ## Grafico solo de regiones
        groupbys = ["region", "cod_region", "fecha"]
        title_txt = "Casos por región"
        str_hover_1 = "<span style='font-size:16px'><b>Región: %{customdata[0]}</b></span><br><br>"
        str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
        color_default = "region"
        custom_default = ["region"]
        data_tmp = df[df.cod_region.isin(region_flt)]
    elif regiones and comunas:
        # Grafico de regones y comunas
        groupbys = ["comuna", "region", "cod_region", "fecha"]
        title_txt = "Casos por comuna"
        str_hover_1_1 = "<span style='font-size:16px'><b>Comuna: %{customdata[0]}</b></span><br><br>"
        str_hover_1_2 = "<span style='font-size:16px'><b>Región: %{customdata[1]}</b></span><br><br>"
        str_hover_1 = str_hover_1_1 + str_hover_1_2
        str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
        color_default = "comuna"
        custom_default = ["comuna", "region"]
        data_tmp = df[(df.cod_region.isin(region_flt)) & (df.comuna.isin(comunas_flt))]
    elif not regiones and comunas:
        error = True
        child = "<br><br><br>Error en la selección."
    # Toques finales
    str_hover = str_hover_1 + str_hover_2 + "<extra></extra>"
    data_flt = data_tmp.groupby(groupbys)["casos"].sum().reset_index()
    fig = px.line(data_flt, x = "fecha", y = "casos", color = color_default, custom_data = custom_default,
                labels = dict_labels, title = title_txt)
    fig.update_layout(showlegend = True)
    fig.update_traces(hovertemplate = str_hover)
    # Retorno de la figura
    if error:
        pass
    else:
        child = dcc.Graph(id = "contagios_comuna",
                            figure = fig,
                            responsive = "auto")
    return child

parrafo = """
Este gráfico muestra la evolución de la cantidad de nuevos contagiados a través de la pandemia,
por comuna, a partir de los informes epidemiológicos publicados por el Ministerio de Salud. La intención
tras este gráfico es determinar la velocidad de aceleración o desaceleración de los contagios, y, por ende,
evaluar las políticas públicas aplicadas durante la pandemia."""
footer = "_Fuente: [Ministerio de Ciencia, Tecnología, Conocimiento e Innovación](https://github.com/MinCiencia/Datos-COVID19)_"

dict_labels = {"comuna": "Comuna", "casos": "# de contagios", "fecha": "Fecha del informe", "region": "Región"}
list_hover = {"region": True, "fecha": "|%d %b %Y", "casos": ":,", "comuna": False}
str_hover_1 = "<span style='font-size:16px'><b>%{customdata[1]}</b></span><br><br>"
str_hover_2 = "<br>".join(["Región: %{customdata[0]}", "Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
str_hover = str_hover_1 + str_hover_2 + "<extra></extra>"
custom_default = ["region", "comuna"]
color_default = "comuna"

region_selec = None
comuna_selec = None

data_comuna, region_dict, comuna_dict = st.data_etl()

layout = dbc.Container(
    children = 
    [
        dbc.Row(
            id = "fila-1-intro",
            children = [
                dbc.Col(
                    id = "columna-1",
                    children = [
                        html.H2(children = "Nuevos contagios"),
                        html.P(children = parrafo, id = "page-desc")
                    ]
                )
            ]
        ),
        dbc.Row(
            id = "fila-2-selectores",
            children = [
                dbc.Col(
                    id = "selectores-region",
                    children = [
                        html.Label(children = "Selecciona una o más regiones:",
                                    id = "small-label"),
                        dcc.Dropdown(
                            id = "regiones",
                            options = [{"label": item["region"], "value": item["cod_region"]} for item in region_dict],
                            value = None,
                            multi = True,
                            placeholder = "Región..."
                        )
                    ]
                ),
                dbc.Col(
                    id = "selectores-comuna",
                    children = [
                        html.Label(children = "Selecciona una o más comunas:",
                                    id = "small-label"),
                        dcc.Dropdown(
                            id = "comunas",
                            options = [{"label": item["comuna"], "value": item["comuna"]} for item in comuna_dict],
                            multi = True,
                            value = None,
                            placeholder = "Comuna..."
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            id = "fila-3-grafico",
            children = 
                [
                    dbc.Col(id = "columna-2-grafico",
                                children = 
                                [
                                    html.Br(),
                                    dcc.Markdown("***En construcción...***"),
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