import dash
import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app

import pandas as pd
from src import setup_etl as st

parrafo = """
Esta tabla muestra los números totales de contagios por región y comuna. La 
funcionalidad de selección de fechas está en proceso de implementación."""
footer = "_Fuente: [Ministerio de Ciencia, Tecnología, Conocimiento e Innovación](https://github.com/MinCiencia/Datos-COVID19)_"

data_comuna, region_dict, comuna_dict = st.data_etl()
data_tbl = data_comuna[["fecha", "region", "comuna", "casos"]]
data_tbl["fecha_d"] = data_tbl["fecha"].dt.strftime("%d %b %Y")
fechas = [pd.to_datetime(item).strftime("%d %b %Y") for item in data_tbl["fecha"].unique()]

layout = dbc.Container(
    children = 
    [
        dbc.Row(
            id = "fila-1-intro",
            children = [
                dbc.Col(
                    id = "columna-1",
                    children = [
                        html.H2(children = "Contagios totales por COVID-19"),
                        html.P(children = parrafo)
                    ]
                )
            ]
        ),
        dbc.Row(
            id = "fila-2-selectores",
            children = [
                dbc.Col(
                    id = "selector-region",
                    children = [
                        html.Label(children = "Selecciona una región:"),
                        dcc.Dropdown(
                            id = "regiones-2",
                            options = [{"label": item["region"], "value": item["region"]} for item in region_dict],
                            value = None,
                            multi = False,
                            placeholder = "Región..."
                        )
                    ]
                ),
                dbc.Col(
                    id = "selector-comuna",
                    children = [
                        html.Label(children = "Selecciona una comuna:"),
                        dcc.Dropdown(
                            id = "comunas-2",
                            options = [{"label": item["comuna"], "value": item["comuna"]} for item in comuna_dict],
                            value = None,
                            multi = False,
                            placeholder = "Comuna..."
                        )
                    ]
                ),
                dbc.Col(
                    id = "selector-fecha",
                    children = [
                        html.Label(children = "Selecciona un rango de fechas:"),
                        dcc.RangeSlider(
                            id = "slider-fechas",
                            min = 0,
                            max = len(fechas) - 1,
                            allowCross = False,
                            value = [0, len(fechas) - 1],
                            step = 1
                        ),
                        html.Div(id = "rango-fechas", style = {"display": "flex", "width": "100%", 
                                                                "padding-bottom": "0.5rem", "font-size": "12px", 
                                                                "justify-content": "center"})
                    ],
                    align = "center"
                ),
            ]
        ),
        dbc.Row(
            id = "fila-2-tabla",
            children = [
                dbc.Col(
                    id = "columna-1-grafico",
                    children = [
                        dash_table.DataTable(
                            id="tabla-contagios",
                            columns = [
                                {"name": "Fecha", "id": "fecha_d", "type": "datetime"},
                                {"name": "Región", "id": "region", "type": "text"},
                                {"name": "Comuna", "id": "comuna", "type": "text"},
                                {"name": "Casos", "id": "casos", "type": "numeric"}
                            ],
                            data = data_tbl.to_dict(orient = "records"),
                            page_size = 40
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            id = "fila-3-footer",
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
    dash.dependencies.Output("rango-fechas", "children"),
    [dash.dependencies.Input("slider-fechas", "value")])
def update_output(value):
    return dcc.Markdown("Filtrando fechas entre {0} y {1}".format(fechas[value[0]], fechas[value[1]]))

@app.callback(
    dash.dependencies.Output("tabla-contagios", "data"),
    [dash.dependencies.Input("regiones-2", "value"),
    dash.dependencies.Input("comunas-2", "value"),
    dash.dependencies.Input("slider-fechas", "value")])
def update_table(region_flt, comunas_flt, rango_fechas):
    # Obteniendo la cantidad de elementos en los filtros
    # # Regiones
    if region_flt is None or len(region_flt) == 0:
        cond_1 = data_tbl.region.notna()
    else:
        cond_1 = data_tbl.region == region_flt
    # # Comunas
    if comunas_flt is None or len(comunas_flt) == 0:
        cond_2 = data_tbl.comuna.notna()
    else:
        cond_2 = data_tbl.comuna == comunas_flt
    # Logica de filtrado
    fecha_min = pd.to_datetime(fechas[rango_fechas[0]], format = "%d %b %Y")
    fecha_max = pd.to_datetime(fechas[rango_fechas[1]], format = "%d %b %Y")
    rango_flt = (data_tbl["fecha"] >= fecha_min) & (data_tbl["fecha"] <= fecha_max)
    return data_tbl[(cond_1) & (cond_2) & (rango_flt) & (data_tbl.casos > 0)].to_dict(orient = "records")

@app.callback(
    dash.dependencies.Output("comunas-2", "options"), 
    [dash.dependencies.Input("regiones-2", "value")])
def actualizar_comunas(region_flt):
    import pandasql as ps
    if region_flt == None:
        return []
    else:
        data_flt = data_comuna[data_comuna.region == region_flt]
        tmp_df = ps.sqldf("SELECT DISTINCT comuna FROM data_flt")
        tmp_dct = tmp_df.to_dict(orient = "records")
        opt = [{"label": item["comuna"], "value": item["comuna"]} for item in tmp_dct]
        return opt