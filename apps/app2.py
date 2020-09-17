import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

import pandas as pd
from src import setup_etl as st

def generate_graph(full_output: bool = False):
    data_comuna, region_dict, comuna_dict = st.data_etl()
    fig = px.line(data_comuna, 
                    x = "fecha", 
                    y = "casos", 
                    color = color_default, 
                    custom_data = custom_default,
                    labels = dict_labels, 
                    title = "Casos totales")
    fig.update_layout(showlegend = False)
    fig.update_traces(hovertemplate = str_hover)
    if full_output:
        return data_comuna, region_dict, comuna_dict, fig
    else:
        return fig

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
Este gráfico muestra la evolución de la cantidad total de contagiados a través de la pandemia,
por comuna, a partir de los informes epidemiológicos publicados por el Ministerio de Salud."""
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

data_comuna, region_dict, comuna_dict, fig = generate_graph(True)

layout = dbc.Container(
    children = 
    [
        dbc.Row(
            id = "fila-1-intro",
            children = [
                dbc.Col(
                    id = "columna-1",
                    children = [
                        html.H2(children = "Evolución de contagios"),
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
            children = [dbc.Col(id = "columna-1-grafico")]
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

@app.callback(Output("comunas", "options"), 
                [Input("regiones", "value")])
def actualizar_selector_comunas(region_flt):
    import pandasql as ps
    if region_flt == None:
        region_flt = []
    data_flt = data_comuna[data_comuna.cod_region.isin(region_flt)]
    tmp_df = ps.sqldf("SELECT DISTINCT comuna FROM data_flt")
    tmp_dct = tmp_df.to_dict(orient = "records")
    opt = [{"label": item["comuna"], "value": item["comuna"]} for item in tmp_dct]
    del data_flt
    return opt

@app.callback(Output("columna-1-grafico", "children"), 
                [Input("regiones", "value"),
                 Input("comunas", "value")])
def actualizar_regiones(region_flt, comunas_flt):
    global region_selec
    global comuna_selec
    region_bool = False
    comuna_bool = False
    # Determinando si fue un mancazo anterior
    if region_flt is None and not comunas_flt is None:
        comunas_flt = None
    else:
        pass
    # Determinando la direccion del cambio de filtros
    cond_reg = region_flt is None or len(region_flt) == 0
    cond_com = comunas_flt is None or len(comunas_flt) == 0
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
    return generar_grafico(df = data_comuna, regiones = region_bool,
                            comunas = comuna_bool, region_flt = region_flt,
                            comunas_flt = comunas_flt)

