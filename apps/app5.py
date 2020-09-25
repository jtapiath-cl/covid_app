import dash
import dash_table

import numpy as np
import pandas as pd
import pandasql as ps
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash_table import Format as dtf
from dash.dependencies import Input, Output

from app import app
from src import setup_etl as st

def obtener_fecha_cercana(df: pd.DataFrame, fecha: pd.Timestamp):
    s = (pd.to_datetime(df["fechas"]) - pd.to_datetime(fecha)).dt.days
    resultado = df.iloc[s[s >= 0].idxmin()]
    return resultado[0]

def obtener_contagios(df: pd.DataFrame, fechas: list):
    val_1 = df[df.fecha == fechas[0]].groupby("fecha")["casos"].sum()[0]
    val_2 = df[df.fecha == fechas[1]].groupby("fecha")["casos"].sum()[0]
    val_3 = df[df.fecha == fechas[2]].groupby("fecha")["casos"].sum()[0]
    val_4 = df[df.fecha == fechas[3]].groupby("fecha")["casos"].sum()[0]
    vals = [int(val_1), int(val_2), int(val_3), int(val_4)]
    return vals

def obtener_diferencias(contagios: list):
    """Se requieren los 4 vaores de totales de contagios para los calculos"""
    c1 = contagios[0]
    c2 = contagios[1]
    c3 = contagios[2]
    c4 = contagios[3]
    abs_dif = [c1 - c2, c1 - c3, c1 - c4]
    rel_dif = [(c1 - c2) * (100 / c2), (c1 - c3) * (100 / c3), (c1 - c4) * (100 / c4)]
    return abs_dif, rel_dif

def generar_tabla(list_contagios: list, list_difs: list, locacion: str):
    ret_df = pd.DataFrame(
        {
            "{0}".format(locacion): ["Total actual", "Informe anterior", "Semana anterior", "Mes anterior"],
            "Casos": ["{0:,}".format(list_contagios[0]), "{0:,}".format(list_contagios[1]), 
                        "{0:,}".format(list_contagios[2]), "{0:,}".format(list_contagios[3])],
            "Diff": ["--", "{0:.2f}%".format(list_difs[0]), "{0:.2f}%".format(list_difs[1]), 
                            "{0:.2f}%".format(list_difs[2])]
        }
    )
    return ret_df

def funcionalidad_principal(hay_region: bool, hay_comuna: bool, graph_tot: bool, 
                            filt_r: str = None, filt_c: str = None):
    etiquetas_t = {"fecha": "Fecha del informe", "casos": "# de contagios"}
    etiquetas_i = {"fecha": "Fecha del informe", "casos": "# de casos/dia"}
    if graph_tot:
        if not hay_region and not hay_comuna:
            data_flt = data_t
            titulo = "Total de contagios"
            etiquetas = etiquetas_t
            tabla_datos_tmp = tabla_1_inicio
        elif hay_region and not hay_comuna:
            filt_data = data_tbl.region == filt_r
            groups = ["region", "fecha"]
            data_flt = data_tbl[filt_data].groupby(groups).sum().reset_index()
            titulo = "Total en {0}".format(filt_r)
            etiquetas = etiquetas_t
            contagios_tmp = obtener_contagios(df=data_flt, fechas=fechas_reportes)
            difs_abs_del, difs_tmp = obtener_diferencias(contagios_tmp)
            del difs_abs_del
            tabla_datos_tmp = generar_tabla(list_contagios = contagios_tmp, list_difs = difs_tmp,
                                            locacion = filt_r)
        elif hay_region and hay_comuna:
            filt_data = (data_tbl.region == filt_r) & (data_tbl.comuna == filt_c)
            groups = ["region", "comuna", "fecha"]
            data_flt = data_tbl[filt_data].groupby(groups).sum().reset_index()
            titulo = "Total en {1}, {0}".format(filt_r, filt_c)
            etiquetas = etiquetas_t
            contagios_tmp = obtener_contagios(df=data_flt, fechas=fechas_reportes)
            difs_abs_del, difs_tmp = obtener_diferencias(contagios_tmp)
            del difs_abs_del
            tabla_datos_tmp = generar_tabla(list_contagios = contagios_tmp, list_difs = difs_tmp,
                                        locacion = filt_c)
        else:
            pass
    else:
        if not hay_region and not hay_comuna:
            data_flt = data_tbl.groupby("fecha")["casos"].sum().diff(periods = 1).reset_index()
            titulo = "Aumento de contagios"
            etiquetas = etiquetas_i
            tabla_datos_tmp = tabla_1_inicio
        elif hay_region and not hay_comuna:
            filt_data = data_tbl.region == filt_r
            groups = ["region", "fecha"]
            data_flt = data_tbl[filt_data].groupby(groups).sum().diff(periods = 1).reset_index()
            data_flt_no_dif = data_tbl[filt_data].groupby(groups).sum().reset_index()
            titulo = "Aumento en region {0}".format(filt_r)
            etiquetas = etiquetas_i
            contagios_tmp = obtener_contagios(df=data_flt_no_dif, fechas=fechas_reportes)
            difs_abs_del, difs_tmp = obtener_diferencias(contagios_tmp)
            del difs_abs_del
            tabla_datos_tmp = generar_tabla(list_contagios = contagios_tmp, list_difs = difs_tmp,
                                            locacion = filt_r)
        elif hay_region and hay_comuna:
            filt_data = (data_tbl.region == filt_r) & (data_tbl.comuna == filt_c)
            groups = ["region", "fecha"]
            data_flt = data_tbl[filt_data].groupby(groups).sum().diff(periods = 1).reset_index()
            data_flt_no_dif = data_tbl[filt_data].groupby(groups).sum().reset_index()
            titulo = "Aumento en {1}, {0}".format(filt_r, filt_c)
            etiquetas = etiquetas_i
            contagios_tmp = obtener_contagios(df=data_flt_no_dif, fechas=fechas_reportes)
            difs_abs_del, difs_tmp = obtener_diferencias(contagios_tmp)
            del difs_abs_del
            tabla_datos_tmp = generar_tabla(list_contagios = contagios_tmp, list_difs = difs_tmp,
                                            locacion = filt_c)
        else:
            pass
    fig = px.line(data_flt, x = "fecha", y = "casos", title = titulo, labels = etiquetas)
    fig.update_traces(hovertemplate = str_hover)
    fig.update_layout(showlegend = False)
    return fig, tabla_datos_tmp
    


data_tbl, regiones, comunas = st.data_etl()

parrafo_1 = """El objetivo de este tablero es mostrar la evolución de los contagios confirmados
de coronavirus en Chile, tanto a nivel nacional, como por región y a nivel comunal."""
parrafo_2 = """Los datos aquí presentados muestran sólo la cantidad de contagios confirmados totales, 
a nivel de comuna. Otras métricas, como la cantidad de sospechas o de fallecimientos, serán incluidos en
futuras iteraciones de la aplicación."""
parrafo_3 = """Es importante notar que la fuente de datos para estos gráficos son los informes epidemiológicos,
por lo que los datos no están disponibles diariamente, y por tanto, no pueden compararse fácilmente
con la información entregada en los reportes que realiza tres veces a la semana el Ministerio."""
parrafo = [html.Br(), html.P(parrafo_1), html.P(parrafo_2), html.P(parrafo_3)]
footer = """
_Fuente: [Ministerio de Ciencia, Tecnología, Conocimiento e Innovación](https://github.com/MinCiencia/Datos-COVID19)_  
_*_: Los reportes epidemiológicos no se emiten todos los días, por lo que las fechas pueden no ser exactamente un día,
una semana o un mes atrás, pero representan la mejor aproximación posible con los datos disponibles."""

date_fmt = "%d %b %Y"

region_sel = None
comuna_sel = None

fechas = pd.DataFrame(data_tbl.fecha.unique(), columns = ["fechas"])

fecha_reporte = max(data_tbl.fecha)
reporte_anterior = pd.to_datetime(np.sort(data_tbl.fecha.unique())[-2])
semana_pasada = obtener_fecha_cercana(df = fechas, fecha = (max(data_tbl.fecha) - pd.to_timedelta(7, unit = "d")).date())
mes_pasado = obtener_fecha_cercana(df = fechas, fecha = (max(data_tbl.fecha) - pd.DateOffset(months = 1)).date())

fechas_reportes = [fecha_reporte, reporte_anterior, semana_pasada, mes_pasado]

contagios = obtener_contagios(df = data_tbl, fechas = fechas_reportes)

dif_abs, dif_rel = obtener_diferencias(contagios)

texto_contagios = "## Contagios totales confirmados en Chile: {0:,}".format(contagios[0])
texto_fecha = [html.H3("Fecha del último reporte:", style = {"margin": "0"}),
                html.H5("{0}".format(fecha_reporte.strftime(date_fmt)), style = {"margin": "0", "text-align": "center"})]

texto_head = """
#### Incremento {interv}  
Fecha del reporte: {fecha}  
Total de contagios: {total:,}  
Incremento a la fecha: {nuevos:,}  
Incremento (%) : {perc:.2f}%
"""
str_hover_1 = "<span style='font-size:14px'><b>Contagios confirmados</b></span><br><br>"
str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
str_hover = str_hover_1 + str_hover_2 + "<extra></extra>"
data_t = data_tbl \
            .groupby(["fecha"])["casos"] \
            .sum() \
            .reset_index()
fig = px.line(data_t, x = "fecha", y = "casos", title = "Contagios totales a nivel nacional",
                labels = {"fecha": "Fecha del informe", "casos": "# de contagios"})

tabla_1_inicio = generar_tabla(list_contagios = contagios, list_difs = dif_rel, locacion = "Nacional")

##==
layout = [
    dbc.Container(
        children = [
            dbc.Row(
                children = [
                    dbc.Col(
                        children = [
                            html.H2("COVID - Monitor de contagios en Chile"),
                            html.P(parrafo),
                            html.Br()
                        ]
                    )
                ]
            ),
            dbc.Jumbotron(
                children = [
                    dbc.Row(
                        children = [
                            dbc.Col(
                                children = [
                                    dcc.Markdown(texto_contagios)
                                ],
                                width = 8
                            ),
                            dbc.Col(
                                children = [
                                    html.P(texto_fecha)
                                ],
                                width = 4
                            )
                        ],
                        id = "totales-inicio"
                    ),
                    dbc.Row(
                        children = [
                            dbc.Col(
                                children = [
                                    dcc.Markdown(
                                        texto_head.format(
                                            fecha = reporte_anterior.strftime(date_fmt),
                                            total = contagios[1],
                                            nuevos = dif_abs[0],
                                            perc = dif_rel[0],
                                            interv = "diario"
                                        )
                                    )
                                ],
                                id = "aumento-diario-inicio",
                                width = 4,
                                style = {"padding-left": "5rem"}
                            ),
                            dbc.Col(
                                children = [
                                    dcc.Markdown(
                                        texto_head.format(
                                            fecha = semana_pasada.strftime(date_fmt),
                                            total = contagios[2],
                                            nuevos = dif_abs[1],
                                            perc = dif_rel[1],
                                            interv = "semanal"
                                        )
                                    )
                                ],
                                id = "aumento-semanal-inicio",
                                width = 4,
                                style = {"padding-left": "2rem",
                                            "padding-right": "2rem"}
                            ),
                            dbc.Col(
                                children = [
                                    dcc.Markdown(
                                        texto_head.format(
                                            fecha = mes_pasado.strftime(date_fmt),
                                            total = contagios[3],
                                            nuevos = dif_abs[2],
                                            perc = dif_rel[2],
                                            interv = "mensual"
                                        )
                                    )
                                ],
                                id = "aumento-mensual-inicio",
                                width = 4,
                                style = {"paddig-left": "5rem"}
                            )
                        ],
                        id = "aumentos-inicio",
                        style = {"padding-top": "1rem", "margin-bottom": "2rem"}
                    ),
                    dbc.Row(
                        children = [
                            dbc.Col(
                                children = [
                                    dbc.Row(
                                        dbc.Col(
                                            children = [
                                                html.Label("Selecciona una región:"),
                                                dcc.Dropdown(
                                                    id = "regiones-inicio",
                                                    options = [{"label": item["region"], "value": item["region"]} for item in regiones],
                                                    value = None,
                                                    multi = False,
                                                    placeholder = "Región..."
                                                )
                                            ]
                                        ),
                                        style = {"padding-top": "1rem", "padding-bottom": "1rem"}
                                    ),
                                    dbc.Row(
                                        dbc.Col(
                                            children = [
                                                html.Label("Selecciona una comuna:"),
                                                dcc.Dropdown(
                                                    id = "comunas-inicio",
                                                    options = [{"label": item["comuna"], "value": item["comuna"]} for item in comunas],
                                                    value = None,
                                                    multi = False,
                                                    placeholder = "Comuna..."
                                                )
                                            ]
                                        ),
                                        style = {"padding-top": "1rem", "padding-bottom": "1rem"}
                                    ),
                                    dbc.Row(
                                        dbc.Col(
                                            children = [
                                                html.Label("Selecciona el tipo de gráfico:"),
                                                dcc.RadioItems(
                                                    options = [
                                                        {"label": "  Contagios totales", "value": "tot"},
                                                        {"label": "  Aumento de contagios", "value": "inc"}
                                                    ],
                                                    value = "tot",
                                                    id = "tipo-grafico-inicio"
                                                )
                                            ]
                                        ),
                                        style = {"padding-top": "1rem", "padding-bottom": "1rem"}
                                    )
                                ],
                                id = "selectores-inicio",
                                width = 3
                            ),
                            dbc.Col(
                                children = [
                                    dcc.Graph(figure = fig),
                                ],
                                id = "grafico-inicio"
                            ),
                            dbc.Col(
                                children = [
                                    dbc.Table.from_dataframe(
                                        tabla_1_inicio,
                                        striped = True,
                                        bordered = True,
                                        hover = True,
                                        responsive = True,
                                        size = "md"
                                    )
                                ],
                                id = "totales-2-inicio",
                                width = 3
                            )
                        ],
                        id = "contenido-inicio"
                    )
                ]
            ),
            dbc.Row(
                id = "footer-inicio",
                children = dcc.Markdown(footer)
            )
        ]
    )
]

@app.callback(
    Output("comunas-inicio", "options"), 
    Input("regiones-inicio", "value")
)
def actualizar_selector_comunas(region_flt):
    import pandasql as ps
    if region_flt == None:
        return []
    data_flt = data_tbl[data_tbl.region == region_flt]
    tmp_df = ps.sqldf("SELECT DISTINCT comuna FROM data_flt")
    tmp_dct = tmp_df.to_dict(orient = "records")
    opt = [{"label": item["comuna"], "value": item["comuna"]} for item in tmp_dct]
    del data_flt
    return opt

@app.callback(
    [
        Output("grafico-inicio", "children"),
        Output("totales-2-inicio", "children")
    ],
    [
        Input("regiones-inicio", "value"),
        Input("comunas-inicio", "value"),
        Input("tipo-grafico-inicio", "value")
    ]
)
def actualizar_dashboard(region_flt, comuna_flt, tipo_grafico):
    global region_sel
    global comuna_sel
    print(region_sel, region_flt)
    print(comuna_sel, comuna_flt)
    # Copio la logica de la app 3
    region_bool = False
    comuna_bool = False
    # Determinando si fue un mancazo anterior
    if region_flt is None and not comuna_flt is None:
        comuna_flt = None
    elif region_flt != region_sel and (comuna_sel is None and not comuna_flt is None):
        comuna_flt = None
        print("Eureka!")
    else:
        pass
    # Determinando la direccion del cambio de filtros
    cond_reg = region_flt is None
    cond_com = comuna_flt is None
    if region_flt == region_sel:
        if cond_reg and cond_com:
            filtro_reg = None
            filtro_com = None
        elif not cond_reg and cond_com:
            region_bool = True
            filtro_reg = region_flt
            filtro_com = None
        elif not cond_reg and not cond_com:
            region_bool = True
            comuna_bool = True
            filtro_reg = region_flt
            filtro_com = comuna_flt
        else:
            return "Error en la seleccion"
    else:
        region_sel = region_flt
        if cond_reg and cond_com:
            filtro_reg = None
            filtro_com = None
        elif not cond_reg and cond_com:
            region_bool = True
            filtro_reg = region_flt
            filtro_com = None
        elif not cond_reg and not cond_com:
            region_bool = True
            comuna_bool = True
            filtro_reg = region_flt
            filtro_com = comuna_flt
        else:
            pass
    if tipo_grafico == "tot":
        total = True
    else:
        total = False
    fig, tab = funcionalidad_principal(hay_region = region_bool, hay_comuna = comuna_bool, graph_tot = total,
                                        filt_r = filtro_reg, filt_c = filtro_com)
    region_sel = region_flt
    comuna_sel = comuna_flt
    # Ahora viene la generacion de los objetos
    return dcc.Graph(figure = fig), dbc.Table.from_dataframe(
                    tab,
                    striped = True,
                    bordered = True,
                    hover = True,
                    responsive = True,
                    size = "sm"
                )
        