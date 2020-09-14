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

parrafo = """
Este gráfico muestra la evolución de la cantidad total de contagiados a través de la pandemia,
por comuna, a partir de los informes epidemiológicos publicados por el Ministerio de Salud. La
aplicación permite analizar el comportamiento de comunas dentro de la misma región, y así observar
su comportamiento relativo."""
footer = "_Fuente: [Ministerio de Ciencia, Tecnología, Conocimiento e Innovación](https://github.com/MinCiencia/Datos-COVID19)_"
dict_labels = {"comuna": "Comuna", "casos": "Contagios totales", "fecha": "Fecha del informe", "region": "Región"}
list_hover = {"region": True, "fecha": "|%d %b %Y", "casos": ":,", "comuna": False}
str_hover_1 = "<span style='font-size:16px'><b>%{customdata[1]}</b></span><br><br>"
str_hover_2 = "<br>".join(["Región: %{customdata[0]}", "Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
str_hover = str_hover_1 + str_hover_2 + "<extra></extra>"
custom_default = ["region", "comuna"]
color_default = "comuna"

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
                        html.H2(children = "Contagios totales por COVID-19"),
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
            children = [
                dbc.Col(
                    id = "columna-1-grafico",
                    children = [
                        dcc.Graph(
                            id = "contagios_comuna",
                            figure = fig,
                            responsive = "auto"
                        )
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

@app.callback(Output("contagios_comuna", "figure"), 
                [Input("regiones", "value"),
                 Input("comunas", "value")])
def actualizar_regiones(region_flt, comunas_flt):
    data_comuna, region_dict_tmp, comuna_dict_tmp, fig_tmp = generate_graph(True)
    del region_dict_tmp, comuna_dict_tmp, fig_tmp
    # Asignaciones de variables para la funcion
    title_txt = None
    color_default = "comuna"
    custom_default = ["region", "comuna"]
    str_hover_1 = "<span style='font-size:16px'><b>%{customdata[1]}</b></span><br><br>"
    str_hover_2 = "<br>".join(["Región: %{customdata[0]}", "Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
    legend_show = False
    # Obteniendo la cantidad de elementos en los filtros
    # # Regiones
    try:
        len_regiones = len(region_flt)
    except:
        len_regiones = 0
    # # Comunas
    try:
        len_comunas = len(comunas_flt)
    except:
        len_comunas = 0
    # Logica de funcionamiento
    if len_regiones == 0:
        if len_comunas == 0:
            # Estado inicial del gráfico
            data_flt = data_comuna.groupby(["region", "cod_region", "fecha"])["casos"].sum().reset_index()
            title_txt = "Casos por región"
            str_hover_1 = "<span style='font-size:16px'><b>Región: %{customdata[0]}</b></span><br><br>"
            str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
            color_default = "region"
            custom_default = ["region"]
            legend_show = True
        else:
            # Caso imposible: no puede haber comunas sin regiones
            data_flt = None
    elif len_regiones == 1:
        str_hover_1 = "<span style='font-size:16px'><b>Comuna: %{customdata[0]}</b></span><br><br>"
        str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
        color_default = "comuna"
        custom_default = ["comuna", "region"]
        if len_comunas == 0:
            # Estado inicial del gráfico
            data_tmp = data_comuna.groupby(["region", "cod_region", "fecha"])["casos"].sum().reset_index()
            data_flt = data_tmp[data_tmp.cod_region.isin(region_flt)]
            str_hover_1 = "<span style='font-size:16px'><b>Región: %{customdata[0]}</b></span><br><br>"
            str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
            color_default = "region"
            custom_default = ["region"]
            legend_show = True
            title_txt = "Casos en regiones seleccionadas"
        else:
            # Una sola region ha sido elegida, se muestran solo las comunas elegidas sin leyenda
            data_flt = data_comuna[(data_comuna.cod_region.isin(region_flt)) & (data_comuna.comuna.isin(comunas_flt))]
            title_txt = "Casos en comunas seleccionadas"
            legend_show = True
    elif len_regiones > 1:
        # Mas de una region ha sido elegida
        if len_comunas == 0:
            # Estado inicial del gráfico
            data_tmp = data_comuna.groupby(["region", "cod_region", "fecha"])["casos"].sum().reset_index()
            data_flt = data_tmp[data_tmp.cod_region.isin(region_flt)]
            str_hover_1 = "<span style='font-size:16px'><b>Región: %{customdata[0]}</b></span><br><br>"
            str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
            color_default = "region"
            custom_default = ["region"]
            legend_show = True
            title_txt = "Casos en regiones seleccionadas"
        else:
            # Mas de una region, mas de una comuna
            data_flt = data_comuna[(data_comuna.cod_region.isin(region_flt)) & (data_comuna.comuna.isin(comunas_flt))]
            title_txt = "Casos en comunas seleccionadas"
            str_hover_1_1 = "<span style='font-size:16px'><b>Comuna: %{customdata[0]}</b></span><br><br>"
            str_hover_1_2 = "<span style='font-size:16px'><b>Región: %{customdata[1]}</b></span><br><br>"
            str_hover_1 = str_hover_1_1 + str_hover_1_2
            str_hover_2 = "<br>".join(["Fecha: %{x|%d %b %Y}", "Casos: %{y:,}"])
            legend_show = True
            custom_default = ["comuna", "region"]
            color_default = "comuna"
    else:
        # Control de flujos, sin impacto en el gráfico
        data_flt = None
    # Toques finales
    str_hover = str_hover_1 + str_hover_2 + "<extra></extra>"
    fig = px.line(data_flt, x = "fecha", y = "casos", color = color_default, custom_data = custom_default,
                labels = dict_labels, title = title_txt)
    fig.update_layout(showlegend = legend_show)
    fig.update_traces(hovertemplate = str_hover)
    return fig

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