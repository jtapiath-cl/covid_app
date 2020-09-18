import dash
import dash_table

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dash_table import Format as dtf
from dash.dependencies import Input, Output

from app import app
from src import setup_etl as st

def get_formatted_date(prev_date: str):
    return prev_date.strftime("%d %b %Y")

def generate_data():
    data_comuna, region_dict, comuna_dict = st.data_etl()
    data_tbl = data_comuna[["fecha", "region", "comuna", "casos", "cod_region"]]
    fechas_tmp = data_tbl.apply(lambda row: get_formatted_date(row.fecha), axis = 1)
    data_tbl = data_tbl.assign(fecha_d = fechas_tmp)
    fechas = [pd.to_datetime(item).strftime("%d %b %Y") for item in data_tbl["fecha"].unique()]
    del fechas_tmp, data_comuna
    return data_tbl, fechas, region_dict, comuna_dict

def generador_tabla(tipo: int, df: pd.DataFrame):
    if tipo == 1:
        # tipo == 1 : grafico a nivel de fecha
        ret_tbl = True
        groupbys = ["fecha", "fecha_d"]
        columnas_req = [{"name": "Fecha", "id": "fecha_d", "type": "datetime"},
                        {"name": "Casos", "id": "casos", "type": "numeric", "format": dtf.Format(group = ",")}]
        data_tbl = df.groupby(groupbys)["casos"].sum() \
                    .reset_index() \
                    .sort_values(by = ["fecha"])
    elif tipo == 2:
        # tipo == 2 : grafico a nivel de region
        ret_tbl = True
        groupbys = ["fecha", "fecha_d", "region"]
        columnas_req = [{"name": "Fecha", "id": "fecha_d", "type": "datetime"},
                        {"name": "Región", "id": "region", "type": "text"},
                        {"name": "Casos", "id": "casos", "type": "numeric", "format": dtf.Format(group = ",")}]
        data_tbl = df.groupby(groupbys)["casos"].sum() \
                    .reset_index() \
                    .sort_values(by = ["fecha"])
    elif tipo == 3:
        # tipo == 3 : grafico a nivel de comuna
        ret_tbl = True
        groupbys = ["fecha", "fecha_d", "region", "comuna"]
        columnas_req = [{"name": "Fecha", "id": "fecha_d", "type": "datetime"},
                        {"name": "Región", "id": "region", "type": "text"},
                        {"name": "Comuna", "id": "comuna", "type": "text"},
                        {"name": "Casos", "id": "casos", "type": "numeric", "format": dtf.Format(group = ",")}]
        data_tbl = df.groupby(groupbys)["casos"].sum() \
                        .reset_index() \
                        .sort_values(by = ["fecha", "comuna"])
    else:
        # otro tipo : retorna un texto
        ret_tbl = False
        texto = "Error en la selección"
    if ret_tbl:
        tabla = dash_table.DataTable(
                    id="tabla-contagios",
                    columns = columnas_req,
                    data = data_tbl.to_dict(orient = "records"),
                    page_size = 40
                )
    else:
        tabla = texto
    return tabla

parrafo = """
Esta tabla muestra los números totales de contagios por fecha, región y comuna. Se puede seleccionar
sólo una región, y dentro de ella, sólo una comuna. La cantidad de casos en la columna "Casos"
es la cantidad de contagios totales a la fecha del informe epidemiológico respectivo.
"""
footer = "_Fuente: [Ministerio de Ciencia, Tecnología, Conocimiento e Innovación](https://github.com/MinCiencia/Datos-COVID19)_"

region_selec = None
comuna_selec = None

data_tbl, fechas, region_dict, comuna_dict = generate_data()

layout = dbc.Container(
    children = 
    [
        dbc.Row(
            id = "pag-1-fila-1-intro",
            children = [
                dbc.Col(
                    id = "pag-1-columna-1",
                    children = [
                        html.H2(children = "Contagios totales"),
                        html.P(children = parrafo, id = "pag-1-page-desc")
                    ]
                )
            ]
        ),
        dbc.Row(
            id = "pag-1-fila-2-selectores",
            children = [
                dbc.Col(
                    id = "pag-1-selector-region",
                    children = [
                        html.Label(children = "Selecciona una región:", id = "pag-1-small-label-region"),
                        dcc.Dropdown(
                            id = "pag-1-regiones-2",
                            options = [{"label": item["region"], "value": item["region"]} for item in region_dict],
                            value = None,
                            multi = False,
                            placeholder = "Región..."
                        )
                    ]
                ),
                dbc.Col(
                    id = "pag-1-selector-comuna",
                    children = [
                        html.Label(children = "Selecciona una comuna:", id = "pag-1-small-label-comuna"),
                        dcc.Dropdown(
                            id = "pag-1-comunas-2",
                            options = [{"label": item["comuna"], "value": item["comuna"]} for item in comuna_dict],
                            value = None,
                            multi = False,
                            placeholder = "Comuna..."
                        )
                    ]
                ),
                dbc.Col(
                    id = "pag-1-selector-fecha",
                    children = [
                        html.Label(children = "Selecciona un rango de fechas:", id = "pag-1-small-label-fecha"),
                        html.Div(
                            dcc.RangeSlider(
                                id = "pag-1-slider-fechas",
                                min = 0,
                                max = len(fechas) - 1,
                                allowCross = False,
                                value = [0, len(fechas) - 1],
                                step = 1
                            ),
                            id = "pag-1-real-selector"
                        ),
                        html.Div(id = "pag-1-rango-fechas", style = {"display": "flex", "width": "100%", 
                                                                        "padding-bottom": "0.5rem", "font-size": "10px", 
                                                                        "justify-content": "center"})
                    ],
                    align = "center"
                )
            ]
        ),
        dbc.Row(
            id = "pag-1-fila-2-tabla",
            children = [dbc.Col(id = "pag-1-columna-1-tabla")]
        ),
        dbc.Row(
            id = "pag-1-fila-3-footer",
            children = [
                dbc.Col(
                    id = "pag-1-columna-1-footer",
                    children = [dcc.Markdown(children = footer)]
                )
            ]
        )
    ]
)

@app.callback(
    Output("pag-1-rango-fechas", "children"),
    Input("pag-1-slider-fechas", "value")
)
def update_output(value):
    return dcc.Markdown("Filtrando fechas entre {0} y {1}".format(fechas[value[0]], fechas[value[1]]))

@app.callback(
    Output("pag-1-comunas-2", "options"), 
    Input("pag-1-regiones-2", "value")
)
def actualizar_comunas(region_flt):
    import pandasql as ps
    if region_flt == None:
        return []
    else:
        data_flt = data_tbl[data_tbl.region == region_flt]
        tmp_df = ps.sqldf("SELECT DISTINCT comuna FROM data_flt")
        tmp_dct = tmp_df.to_dict(orient = "records")
        opt = [{"label": item["comuna"], "value": item["comuna"]} for item in tmp_dct]
        del data_flt
        return opt

@app.callback(
    Output("pag-1-columna-1-tabla", "children"),
    [
        Input("pag-1-regiones-2", "value"),
        Input("pag-1-comunas-2", "value"),
        Input("pag-1-slider-fechas", "value")
    ]
)
def update_table(region_flt, comunas_flt, rango_fechas):
    global region_selec
    global comuna_selec
    if region_selec == region_flt:
        # No ha cambiado la region
        execute = True
    else:
        # Cambio la seleccion de region
        if region_flt is None:
            # Se limpio la region
            tipo = 1
            execute = False
            region_selec = region_flt
            cond_1 = data_tbl.region.notna()
            cond_2 = data_tbl.comuna.notna()
        else:
            # Solo cambio la region
            tipo = 2
            execute = False
            region_selec = region_flt
            cond_1 = data_tbl.region == region_flt
            cond_2 = data_tbl.comuna.notna()
    if execute:
        # Tipo de tabla a mostrar
        tipo = 0
        if region_flt is None or len(region_flt) == 0:
            tipo = 1
        else:
            if comunas_flt is None or len(comunas_flt) == 0:
                tipo = 2
            else:
                tipo = 3
        # # Regiones
        if region_flt is None or len(region_flt) == 0:
            cond_1 = data_tbl.region.notna()
        else:
            cond_1 = data_tbl.region == region_flt
        # # Comunas
        if comunas_flt is None or len(comunas_flt) == 0:
            cond_2 = data_tbl.comuna.notna()
        else:
            comuna_selec = comunas_flt
            cond_2 = data_tbl.comuna == comunas_flt
    else:
        pass
    # Logica de filtrado
    fecha_min = pd.to_datetime(fechas[rango_fechas[0]], format = "%d %b %Y")
    fecha_max = pd.to_datetime(fechas[rango_fechas[1]], format = "%d %b %Y")
    rango_flt = (data_tbl["fecha"] >= fecha_min) & (data_tbl["fecha"] <= fecha_max)
    return_df = data_tbl[(cond_1) & (cond_2) & (rango_flt) & (data_tbl.casos > 0)]
    return generador_tabla(tipo = tipo, df = return_df)