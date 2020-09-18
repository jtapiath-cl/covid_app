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
    del fechas_tmp
    return data_tbl, fechas, region_dict, comuna_dict

def generar_grafico(df: pd.DataFrame, regiones: bool = False, comunas: bool = False,
                    region_flt = None, comunas_flt = None):
    error = False
    dict_labels = {"comuna": "Comuna", "casos": "# de contagios", "fecha": "Fecha del informe", "region": "Región"}
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
        title_txt = "Casos nuevos a nivel regional"
        str_hover_1 = "<span style='font-size:16px'><b>Región: %{customdata[0]}</b></span><br><br>"
        str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
        color_default = "region"
        custom_default = ["region"]
        data_tmp = df[df.cod_region == region_flt]
    elif regiones and comunas:
        # Grafico de regones y comunas
        groupbys = ["region", "cod_region", "comuna", "fecha"]
        title_txt = "Casos nuevos a nivel comunal"
        str_hover_1_1 = "<span style='font-size:16px'><b>Comuna: %{customdata[0]}</b></span><br><br>"
        str_hover_1_2 = "<span style='font-size:16px'><b>Región: %{customdata[1]}</b></span><br><br>"
        str_hover_1 = str_hover_1_1 + str_hover_1_2
        str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
        color_default = "comuna"
        custom_default = ["comuna", "region"]
        data_tmp = df[(df.cod_region == region_flt) & (df.comuna == comunas_flt)]
    elif not regiones and comunas:
        error = True
        child = "<br><br><br>Error en la selección."
    # Retorno de la figura
    if error:
        pass
    else:
        # Toques finales
        str_hover = str_hover_1 + str_hover_2 + "<extra></extra>"
        data_flt = data_tmp.groupby(groupbys)["casos"] \
                        .sum() \
                        .diff(periods = 1) \
                        .reset_index()
        fig = px.line(data_flt, x = "fecha", y = "casos", color = color_default, custom_data = custom_default,
                    labels = dict_labels, title = title_txt)
        fig.update_layout(showlegend = False)
        fig.update_traces(hovertemplate = str_hover)
        child = dcc.Graph(id = "contagios-comuna-inc",
                            figure = fig,
                            responsive = "auto")
    return child

def generar_tabla(df: pd.DataFrame, regiones: bool = False, comunas: bool = False,
                    region_flt = None, comunas_flt = None):
    error = False
    if not regiones and not comunas:
        data_tmp = df
        grps = ["fecha", "fecha_d"]
        columnas_tbl = [{"name": "Fecha", "id": "fecha_d", "type": "datetime"},
                        {"name": "Casos", "id": "casos", "type": "numeric", "format": dtf.Format(group = ",")}]
    elif regiones and not comunas:
        flt = df.cod_region == region_flt
        data_tmp = df[flt]
        grps = ["region", "cod_region", "fecha", "fecha_d"]
        columnas_tbl = [{"name": "Fecha", "id": "fecha_d", "type": "datetime"},
                        {"name": "Región", "id": "region", "type": "text"},
                        {"name": "Casos", "id": "casos", "type": "numeric", "format": dtf.Format(group = ",")}]
    elif regiones and comunas:
        flt_1 = df.cod_region == region_flt
        flt_2 = df.comuna == comunas_flt
        data_tmp = df[(flt_1) & (flt_2)]
        grps = ["region", "cod_region", "comuna", "fecha", "fecha_d"]
        columnas_tbl = [{"name": "Fecha", "id": "fecha_d", "type": "datetime"},
                        {"name": "Región", "id": "region", "type": "text"},
                        {"name": "Comuna", "id": "comuna", "type": "text"},
                        {"name": "Casos", "id": "casos", "type": "numeric", "format": dtf.Format(group = ",")}]
    else:
        error = True
        child = "<br><br><br>Error en la selección."
    if error:
        pass
    else:
        data_grp = data_tmp.groupby(grps)["casos"] \
                    .sum() \
                    .diff(periods = 1) \
                    .reset_index()
        child = dash_table.DataTable(
                    id="tabla-contagios-inc",
                    columns = columnas_tbl,
                    data = data_grp.to_dict(orient = "records"),
                    page_size = 15
                )
    return child

parrafo = """
Este gráfico muestra la evolución de la cantidad de nuevos contagiados a través de la pandemia,
por región o comuna, a partir de los informes epidemiológicos publicados por el Ministerio de Salud. La intención
tras este gráfico es determinar la velocidad de aceleración o desaceleración de los contagios, y, por ende,
evaluar las políticas públicas aplicadas durante la pandemia."""
footer = "_Fuente: [Ministerio de Ciencia, Tecnología, Conocimiento e Innovación](https://github.com/MinCiencia/Datos-COVID19)_"

region_selec = None
comuna_selec = None

data_tbl, fechas, region_dict, comuna_dict = generate_data()

layout = dbc.Container(
    children = 
    [
        dbc.Row(
            id = "pag-3-fila-1-intro",
            children = [
                dbc.Col(
                    id = "pag-3-columna-1",
                    children = [
                        html.H2(children = "Incremento de contagios"),
                        html.P(children = parrafo, id = "pag-3-page-desc")
                    ]
                )
            ]
        ),
        dbc.Row(
            id = "pag-3-fila-2-selectores",
            children = [
                dbc.Col(
                    id = "pag-3-selectores-region",
                    children = [
                        html.Label(children = "Selecciona una región:",
                                    id = "pag-3-small-label"),
                        dcc.Dropdown(
                            id = "pag-3-regiones",
                            options = [{"label": item["region"], "value": item["cod_region"]} for item in region_dict],
                            value = None,
                            multi = False,
                            placeholder = "Región..."
                        )
                    ]
                ),
                dbc.Col(
                    id = "pag-3-selectores-comuna",
                    children = [
                        html.Label(children = "Selecciona una comuna:",
                                    id = "pag-3-small-label"),
                        dcc.Dropdown(
                            id = "pag-3-comunas",
                            options = [{"label": item["comuna"], "value": item["comuna"]} for item in comuna_dict],
                            value = None,
                            multi = False,
                            placeholder = "Comuna..."
                        )
                    ]
                ),
                dbc.Col(
                    id = "pag-3-selector-fecha",
                    children = [
                        html.Label(children = "Selecciona un rango de fechas:", id = "pag-3-small-label-fecha"),
                        html.Div(
                            dcc.RangeSlider(
                                id = "pag-3-slider-fechas",
                                min = 0,
                                max = len(fechas) - 1,
                                allowCross = False,
                                value = [0, len(fechas) - 1],
                                step = 1
                            ),
                            id = "pag-3-real-selector"
                        ),
                        html.Div(id = "pag-3-rango-fechas", style = {"display": "flex", "width": "100%", 
                                                                        "padding-bottom": "0.5rem", "font-size": "10px", 
                                                                        "justify-content": "center"})
                    ],
                    align = "center"
                )
            ]
        ),
        dbc.Row(
            id = "pag-3-fila-3-grafico",
            children = 
                [
                    dbc.Col(id = "pag-3-columna-2-grafico"),
                    dbc.Col(id = "pag-3-columna-2-tabla")
                ]
        ),
        dbc.Row(
            id = "pag-3-fila-4-footer",
            children = [
                dbc.Col(
                    id = "pag-3-columna-1-footer",
                    children = [dcc.Markdown(children = footer)]
                )
            ]
        )
    ]
)

@app.callback(
    Output("pag-3-rango-fechas", "children"),
    Input("pag-3-slider-fechas", "value")
)
def update_output(value):
    return dcc.Markdown("Filtrando fechas entre {0} y {1}".format(fechas[value[0]], fechas[value[1]]))

@app.callback(
    Output("pag-3-comunas", "options"), 
    Input("pag-3-regiones", "value")
)
def actualizar_selector_comunas(region_flt):
    import pandasql as ps
    if region_flt == None:
        return []
    data_flt = data_tbl[data_tbl.cod_region == region_flt]
    tmp_df = ps.sqldf("SELECT DISTINCT comuna FROM data_flt")
    tmp_dct = tmp_df.to_dict(orient = "records")
    opt = [{"label": item["comuna"], "value": item["comuna"]} for item in tmp_dct]
    del data_flt
    return opt

@app.callback(
    [
        Output("pag-3-columna-2-grafico", "children"),
        Output("pag-3-columna-2-tabla", "children")
    ],
    [
        Input("pag-3-regiones", "value"),
        Input("pag-3-comunas", "value"),
        Input("pag-3-slider-fechas", "value")
    ]

)
def actualizar_datos(region_flt, comuna_flt, rango_fechas):
    global region_selec
    global comuna_selec
    region_bool = False
    comuna_bool = False
    # Determinando si fue un mancazo anterior
    if region_flt is None and not comuna_flt is None:
        comuna_flt = None
    else:
        pass
    # Determinando la direccion del cambio de filtros
    cond_reg = region_flt is None
    cond_com = comuna_flt is None
    if region_flt == region_selec:
        if cond_reg and cond_com:
            pass
        elif not cond_reg and cond_com:
            region_bool = True
        elif not cond_reg and not cond_com:
            region_bool = True
            comuna_bool = True
        else:
            return "Error en la seleccion"
    else:
        region_selec = region_flt
        if cond_reg and cond_com:
            pass
        elif not cond_reg and cond_com:
            region_bool = True
        elif not cond_reg and not cond_com:
            region_bool = True
            comuna_bool = True
        else:
            pass
    fecha_min = pd.to_datetime(fechas[rango_fechas[0]], format = "%d %b %Y")
    fecha_max = pd.to_datetime(fechas[rango_fechas[1]], format = "%d %b %Y")
    rango_flt = (data_tbl["fecha"] >= fecha_min) & (data_tbl["fecha"] <= fecha_max)
    data_flt = data_tbl[rango_flt]
    return_1 = generar_grafico(df = data_flt, regiones = region_bool,
                comunas = comuna_bool, region_flt = region_flt,
                comunas_flt = comuna_flt)
    return_2 = generar_tabla(df = data_flt, regiones = region_bool,
                comunas = comuna_bool, region_flt = region_flt,
                comunas_flt = comuna_flt)
    return return_1, return_2
        