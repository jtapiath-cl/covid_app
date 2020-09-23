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
from src import setup_etl as se

data_comunas, regiones, comunas = se.data_etl()
del regiones, comunas

dict_labels = {"comuna": "Comuna", "casos": "# de contagios", "fecha": "Fecha del informe", "region": "Región"}
filt_reg = data_comunas.region == "Magallanes"
filt_pa = data_comunas.comuna == "Punta Arenas"
filt_not_pa = data_comunas.comuna != "Punta Arenas"

# Recordatorio: en Markdown, un <br> es dos espacios y un enter
header = """**Fecha del análisis**: 2020-09-23  
**Tema**: Curva de contagios en la región de Magallanes"""
p_1 = """##### **Discusión**:  
El 21 de septiembre de 2020, el intendente de la región de Magallanes y Antártica
Chilena, José Fernández Dübrock, presentó su renuncia al cargo. Durante sus últimos días
como autoridad regional, parte de la atención del manejo de la pandemia
se había centrado en la gran cantidad de contagios que se presentaban en dicha
región, particularmente en la comuna de Punta Arenas. Siendo una
de las primeras comunas en haber avanzado en el plan Paso a Paso hacia el desconfinamiento, el 21 de
agosto volvió a entrar en Cuarentena, como consta en 
[múltiples](https://laprensaaustral.cl/titular1/punta-arenas-vuelve-a-quedar-en-cuarentena-total-desde-este-viernes-a-las-23-horas/)
[artículos](https://elmagallanico.com/2020/08/anuncian-segunda-cuarentena-total-para-punta-arenas)
[de](https://www.t13.cl/noticia/nacional/punta-arenas-retrocedio-fase-cuarentena-05-08-2020)
[prensa](https://www.24horas.cl/regiones/austral/primer-fin-de-semana-de-cuarentena-en-punta-arenas-4380294).
Por ello, el objetivo de este breve análisis es revisar el estado actual de 
los contagios en la región, y en las distintas comunas, junto con algunos
comentarios respecto de las políticas públicas aplicadas en la zona.
"""
p_2 = """
La evolución de contagios en la comuna de Magallanes se puede apreciar
en el siguiente gráfico:
"""
data_g1 = data_comunas[filt_reg] \
            .groupby(["fecha", "region"])["casos"] \
            .sum() \
            .reset_index()
fig_1 = px.line(data_g1, x = "fecha", y = "casos", color = "region", labels = dict_labels,
                title = "Fig 1: Curva de contagios en la región de Magallanes")
fig_1.update_layout(showlegend = False)
p_3 = """
Y la evolución por comunas se ve en los siguientes gráficos: a la izquierda,
Punta Arenas, y a la derecha, las comunas restantes:
"""
data_g2 = data_comunas[(filt_reg) & (filt_pa) ] \
            .groupby(["fecha", "region", "comuna"])["casos"] \
            .sum() \
            .reset_index()
fig_2 = px.line(data_g2, x = "fecha", y = "casos", color = "comuna", labels = dict_labels,
                title = "Fig 2: Curva de contagios en Punta Arenas")
fig_2.update_layout(showlegend = False)
data_g3 = data_comunas[(filt_reg) & (filt_not_pa) ] \
            .groupby(["fecha", "region", "comuna"])["casos"] \
            .sum() \
            .reset_index()
fig_3 = px.line(data_g3, x = "fecha", y = "casos", color = "comuna", labels = dict_labels,
                title = "Fig 3: Curva de contagios fuera de Punta Arenas")
fig_3.update_layout(showlegend = True)
p_4 = "Quizás, más ilustrativo sea ver la velocidad de aumento de casos en las comunas de la región:"
comunas_unique = ps.sqldf("SELECT DISTINCT comuna FROM data_comunas WHERE region = 'Magallanes'") \
                    .to_dict(orient = "records")
data_g4 = pd.DataFrame()
for comuna in data_comunas[filt_reg].comuna.unique():
    data_tmp = data_comunas[(filt_reg) & (data_comunas.comuna == comuna)] \
                .groupby(["fecha", "region", "comuna"])["casos"] \
                .sum() \
                .diff(periods = 1) \
                .reset_index()
    data_g4 = data_g4.append(data_tmp)
    del data_tmp
fig_4 = px.line(data_g4, x = "fecha", y = "casos", color = "comuna", labels = dict_labels,
                title = "Fig 4: Curva de aceleración de contagios por comuna en Magallanes")
p_5 = "Comencemos por analizar el comportamiento de los contagios confirmados en la comuna de Punta Arenas."
p_6 = """
Si miramos la curva de aceleración de contagios, es relativamente claro que, a partir de fines
 de julio, existe un aumento evidente en los contagios, incluso cambiando la forma de la curva.
Es más fácil verlo de manera gráfica:
"""
data_g5 = data_g4[data_g4.comuna == "Punta Arenas"]
fig_5 = px.line(data_g5, x = "fecha", y = "casos", labels = dict_labels, 
                title = "Fig 5: Curva de aceleración de contagios en Punta Arenas")
fig_5.add_shape(dict(type = "line", x0 = "2020-07-25", y0 = 0, x1 = "2020-07-25", y1 = 560))
fig_5.update_shapes(dict(xref='x', yref='y'))
data_g6 = data_g5[data_g5.fecha <= "2020-07-25"]
data_g7 = data_g5[data_g5.fecha >= "2020-07-25"]
fig_6 = px.scatter(data_g6, x = "fecha", y = "casos", labels = dict_labels, 
                    title = "Fig 6: Aceleración hasta el 25 de julio", trendline = "ols",
                    trendline_color_override = "crimson")
fig_7 = px.scatter(data_g7, x = "fecha", y = "casos", labels = dict_labels, 
                    title = "Fig 7: Aceleración desde el 25 de julio", trendline = "ols",
                    trendline_color_override = "crimson")
p_7 = """
Podemos obtener las primeras observaciones experimentales:  
* Durante los primeros 4 meses de pandemia (entre el 1 de abril y el 24 de julio, primera y
última fechas registradas), el manejo de la pandemia fue adecuado, con índices de contagio no 
sólo bajo control sino que, ajustando una línea recta, a la baja. Es decir, los contagios nuevos
_iban decreciendo_, como se ve en la figura 6.
* En estos mismos 4 primeros meses, hubo entre 4 y 92 nuevos contagios por informe, lo que nos habla
de una media centrada en 50. Esto, en términos simples, indica que, en promedio, por día existieron 50
nuevos contagios en la ciudad de Punta Arenas.
* En un análisis algo más técnico, el ajustar una línea recta (o, en terminología estadística, _ajustar
una regresión lineal_ a los datos), para la primera etapa de la pandemia, tiene poco valor predictivo. Si
verificamos el valor del estadístico R², el coeficiente de 0.16 aprox. habla de un ajuste pobre.
* A partir del 25 de julio, y casi a dos meses del hecho, la comuna de Punta Arenas entra en una
 nueva etapa de la pandemia. Todos los informes epidemiológicos entregados a partir de esa fecha, 
 comenzaron a exhibir una tendencia al alza, como se puede apreciar en la figura 7.
* La tendencia al alza, en términos estadísticos, es mucho más ajustada a la realidad de los datos que
la tendencia a la baja de la primera etapa, evidenciada por el estadístico R² y su valor de 0.87.
* Esta alza lineal en la _aceleración_ hace que la curva de contagios totales (figura 3) tenga un crecimiento
denominado _exponencial_ o _palo de hockey_: la tasa a la que crece diariamente el número de contagiados no es
plana, sino que va aumentando.
* Sin más información respecto de las medidas de prevención y mitigación indicadas para la comuna, es difícil
opinar respecto de la efectividad del control de la pandemia. Claramente algo está fallando en la cadena de 
prevención, pues una comuna de 142,000 habitantes, con 500 nuevos contagios diarios estando en estado de 
Cuarentena, nos habla de una población con muy poco autocontrol, de una fiscalización nula y por ende un nivel
de cumplimiento nulo de las medidas de confinamiento, o de niveles de hacinamiento enormes y, por ende, aumento
de contagios muy grandes en la ciudad.
* Sin mayores detalles etnográficos y demográficos de la población contagiada (por ejemplo barrios, edad, nivel
socioeconómico, entre otros datos), se hace muy difícil, a un nivel centralizado, tomar decisiones que permitan
estimar el avance de la pandemia y los niveles de infección en la comuna. Los datos analizados, y de manera
unidimensional (es decir, sólo considerando la cantidad de contagios en el pasado), dan a entender que los 
contagios irían aumentando progresivamente. Esto es irreal, pues hay límites físicos para la cantidad de
contagios que pueden existir. Sin embargo, es claro también que existe una falta de datos enorme hacia el público
general, para poder observar y auditar con mayor claridad lo que ocurre.
* Si fuera sólo por el manejo del nivel de contagios, no es de extrañar que el ahora ex intendente de Magallanes
haya presentado su renuncia. Resulta inaceptable hacia la opinión pública, el deterioro en el nivel de salud
pública de la comuna, en la mitad del tiempo de la primera etapa; en dos meses (entre julio y septiembre), se
retrocedió e incluso empeoró lo que se había mantenido en tan buenas condiciones durante 4 meses de invierno. Esta
observación, por supuesto, está profundamente sesgada con la falta de experiencia en la comuna y la región, pero,
a nivel de números macro, la conclusión es clara.
* Finalmente, es evidente que el comportamiento de la región lo determina el comportamiento de la comuna de Punta
Arenas. Incidentalmente, Punta Arenas es la capital de la región; como el centro urbano de mayor población, esto
tiene sentido. Esto evidencia el riesgo de mostrar datos tan agregados, tan agrupados: si extraemos la ciudad 
de Punta Arenas del análisis, el análisis del manejo de la pandemia tendrá otros tintes, como se ve a continuación.
"""
p_8 = """
Si excluimos la comuna de Punta Arenas del análisis, como se puede ver en la figura 3 (más grande abajo),
podemos observar un comportamiento sumamente distinto al de la comuna de Punta Arenas. Como hipótesis inicial,
podemos postular que la incidencia de la pandemia tiene que ver con la población de cada comuna, que podemos ver
en la tabla siguiente:
"""
data_t1 = data_comunas[(filt_reg) & (filt_not_pa) & (data_comunas.comuna != "Desconocido Magallanes")] \
            .groupby(["region", "comuna"])[["poblacion", "casos"]] \
            .mean() \
            .reset_index() \
            .sort_values(by = "poblacion", ascending = False)
tabla_1 = dash_table.DataTable(
    columns = [{"name": "Comuna", "id": "comuna", "type": "text"},
                {"name": "Población", "id": "poblacion", "type": "numeric", "format": dtf.Format(group = ",")},
                {"name": "Promedio de casos diarios", "id": "casos", "type": "numeric", 
                    "format": dtf.Format(precision = 2, scheme = dtf.Scheme.fixed)}],
    data = data_t1.to_dict(orient = "records"),
    page_size = 10
)
p_9 = """
Claramente hay una correlación entre la población y la incidencia infecciosa del virus, como es de esperar.
Del gráfico anterior, podemos obtener también algunas conclusiones preliminares tambien:  
* Entre agosto y septiembre, se ve un cambio en la curvatura de las curvas de contagios totales. Esto, en
palabras simples, indica que la curva crece de manera más acelerada.
* Natales y Porvenir, como las comunas más pobladas de la región tras Punta Arenas, exhiben la mayor alza
en contagios a partir de las fechas indicadas. Esto, en conjunto con la data observada de Punta Arenas, da pie
para pensar en un aumento en los índices de movilidad importantes.
* Se ven algunos retrocesos en la aceleración (muy leves, de -1 o -2), en comunas como Cabo de Hornos y Primavera.
Esto es indicativo de una desaceleración activa, que trae el cuestionamiento: puede disminuir tan radicalmente
la cantidad de contagios totales en una comuna?
* Finalmente, es necesario monitorear con mayor detalle no sólo el número de casos totales confirmados,
sino también y en mayor detalle los casos sospechosos. Un mayor aumento de casos confirmados implica, por un
lado, un aumento en la cantidad de tests realizados (dato que se podría corroborar), y por otro lado, un aumento
explosivo en la cantidad de casos sospechosos no notificados y/o no confirmados.  

Es imperativo, finalmente y a modo de conclusión, considerar múltiples variables a la hora de realizar análisis
del avance de la pandemia: la cantidad de contagios totales o nuevos no es suficiente para estimar el estado de
una región respecto de la salud de sus habitantes. Dimensiones como la edad, grupos socioeconómicos, profundidad
geográfica mayor, densidad poblacional, índices de movilidad, cantidad de tests realizados, entre otras, son
absolutamente necesarias para poder realizar evaluaciones responsables desde la perspectiva de las políticas públicas.
"""

layout = [
    dcc.Markdown(header),
    dcc.Markdown(p_1), 
    html.Br(),
    dcc.Markdown(p_2),
    dcc.Graph(figure = fig_1),
    dcc.Markdown(p_3),
    dbc.Row(
        children = [
            dbc.Col(
                width = 5,
                children = dcc.Graph(figure = fig_2)
            ),
            dbc.Col(
                width = 7,
                children = dcc.Graph(figure = fig_3)
            )
        ]
    ),
    dcc.Markdown(p_4),
    dbc.Row(
        children = [
            dbc.Col(
                width = 4,
                children = [
                    html.Br(), html.Br(), html.Br(), html.Br(),
                    html.P(
                        children = "Selecciona una comuna de la región de Magallanes y la Antártica Chilena:",
                        style = {"font-size": "12px"}
                    ),
                    dcc.Dropdown(
                        options = [{"label": item["comuna"], "value": item["comuna"]} for item in comunas_unique],
                        multi = False,
                        value = None,
                        id = "dropdown-magallanes-1",
                        placeholder = "Comuna..."
                    )
                ]
            ),
            dbc.Col(
                dcc.Graph(figure = fig_4, id = "magallanes-aceleracion")
            )
        ]
    ),
    dcc.Markdown(p_5),
    html.H4("Punta Arenas"),
    dcc.Markdown(p_6),
    dbc.Row(
        dbc.Col(
            dcc.Graph(figure = fig_5)
        )
    ),
    dbc.Row(
        children = [
            dbc.Col(
                dcc.Graph(figure = fig_6)
            ),
            dbc.Col(
                dcc.Graph(figure = fig_7)
            )
        ]
    ),
    dcc.Markdown(p_7),
    html.H4("Fuera de Punta Arenas"),
    dcc.Markdown(p_8),
    dcc.Graph(figure = fig_3),
    html.H5("Tabla 1: Población y casos promedio diarios por comuna"),
    tabla_1,
    html.Br(),
    dcc.Markdown(p_9)
]

@app.callback(
    Output("magallanes-aceleracion", "figure"),
    Input("dropdown-magallanes-1", "value")
)
def actualizar_grafico_magallanes(filtro_comuna):
    titulo = "Fig 4: Curva de aceleración de contagios por comuna en Magallanes"
    if filtro_comuna is None:
        fig = px.line(data_g4, x = "fecha", y = "casos", color = "comuna", labels = dict_labels,
                        title = titulo)
    else:
        data_tmp = data_comunas[(filt_reg) & (data_comunas.comuna == filtro_comuna)] \
                    .groupby(["fecha", "region", "comuna"])["casos"] \
                    .sum() \
                    .diff(periods = 1) \
                    .reset_index()
        fig = px.line(data_tmp, x = "fecha", y = "casos", color = "comuna", labels = dict_labels,
                        title = titulo)
    return fig