import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

import pandas as pd
from src import setup_etl as st

data_comuna, region_dict, comuna_dict = st.data_etl()
fig = px.line(data_comuna, x = "fecha", y = "casos", color = "comuna")

layout = html.Div(children=[
    html.H1(children = "Progresión de contagiados totales por COVID-19 por comuna"),
    html.P(children = "Este gráfico muestra la cantidad de contagiados acumulados por informe epidemiológico, por comuna."),
    html.Label(children = "Selecciona una región:"),
    dcc.Dropdown(
        id = "regiones",
        options = [{"label": item["region"], "value": item["cod_region"]} for item in region_dict],
        value = None,
        placeholder = "Región..."
    ),
    html.Label(children = "Selecciona una o más comunas:"),
    dcc.Dropdown(
        id = "comunas",
        options = [{"label": item["comuna"], "value": item["comuna"]} for item in comuna_dict],
        multi = True,
        value = None,
        placeholder = "Comuna..."
    ),
    dcc.Graph(
        id = "contagios_comuna",
        figure = fig
    )
])

@app.callback(Output("contagios_comuna", "figure"), 
                [Input("regiones", "value"),
                 Input("comunas", "value")])
def actualizar_regiones(region_flt, comunas_flt):
    try:
        len_comunas = len(comunas_flt)
    except:
        len_comunas = 0
    if region_flt is None:
        fig = px.line(data_comuna, x = "fecha", y = "casos", color = "comuna")
        return fig
    if region_flt is None and comunas_flt is None:
        fig = px.line(data_comuna, x = "fecha", y = "casos", color = "comuna")
        return fig
    if region_flt is not None and (comunas_flt is None or len_comunas == 0):
        data_flt = data_comuna[data_comuna.cod_region == int(region_flt)]
        fig = px.line(data_flt, x = "fecha", y = "casos", color = "comuna")
        return fig
    if region_flt is not None:
        data_flt = data_comuna[(data_comuna.cod_region == int(region_flt)) & (data_comuna.comuna.isin(comunas_flt))]
        fig = px.line(data_flt, x = "fecha", y = "casos", color = "comuna")
        return fig
    if comunas_flt is not None:
        data_flt = data_comuna[data_comuna.comuna.isin(comunas_flt)]
        fig = px.line(data_flt, x = "fecha", y = "casos", color = "comuna")
        return fig

@app.callback(Output("comunas", "options"), 
                [Input("regiones", "value")])
def actualizar_selector_comunas(region_flt):
    import pandasql as ps
    data_flt = data_comuna[data_comuna.cod_region == region_flt]
    tmp_df = ps.sqldf("SELECT DISTINCT comuna FROM data_flt")
    tmp_dct = tmp_df.to_dict(orient = "records")
    opt = [{"label": item["comuna"], "value": item["comuna"]} for item in tmp_dct]
    return opt

# @app.callback(Output("contagios_comuna", "figure"),
#                 [Input("comunas", "value")])
# def actualizar_comunas(valores_comunas):
#     data_flt = data_comuna[data_comuna["comuna"].isin(valores_comunas)]
#     fig = px.line(data_flt, x = "fecha", y = "casos", color = "comuna")
#     return fig