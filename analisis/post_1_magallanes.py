import plotly.express as px
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

# Recordatorio: en Markdown, un <br> es dos espacios y un enter
header = """**Análisis**: 2020-09-21  
**Tema**: Curva de contagios en la región de Magallanes"""
p_1 = """**Discusión**:  
Durante los últimos días, parte de la atención del manejo de la pandemia
se ha centrado en la cantidad de contagios que se presentan en la comuna
de Magallanes, particularmente en la comuna de Punta Arenas. Siendo una
de las primeras comunas en haber avanzado en el plan Paso a Paso, el 21 de
agosto volvió a entrar en Cuarentena, como consta en [múltiples](https://laprensaaustral.cl/titular1/punta-arenas-vuelve-a-quedar-en-cuarentena-total-desde-este-viernes-a-las-23-horas/)
 [artículos](https://elmagallanico.com/2020/08/anuncian-segunda-cuarentena-total-para-punta-arenas)
 [de](https://www.t13.cl/noticia/nacional/punta-arenas-retrocedio-fase-cuarentena-05-08-2020)
 [prensa](https://www.24horas.cl/regiones/austral/primer-fin-de-semana-de-cuarentena-en-punta-arenas-4380294).
Por ello, el objetivo de este breve análisis es revisar el estado actual de 
los contagios en la región, y en las distintas comunas, junto con algunos
comentarios respecto de las políticas públicas aplicadas en la zona.
"""
p_2 = """

"""
layout = [
    dcc.Markdown(header),
    dcc.Markdown(p_1), 
    html.Br(),
    dcc.Markdown(p_2)
]