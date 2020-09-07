# # app.py - a minimal flask api using flask_restful
# from flask import Flask
# from flask_restful import Resource, Api

# app = Flask(__name__)
# api = Api(app)

# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

# api.add_resource(HelloWorld, '/api')

# @app.route('/')
# def hello():
#     return "Hello world!"

# if __name__ == '__main__':
#     app.run(debug = True, host = '0.0.0.0', port = 6000)

# -------------------------
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

# Iniciar la app de Dash (bootstrap!)
app = dash.Dash(__name__)

# Cargar datos a Pandas
df = pd.read_csv("data/data.csv", index_col = 0, parse_dates = True)
df.index = pd.to_datetime(df["fecha"])

# Gráfico de prueba
fig = px.bar(df, x = "fecha", y = "casos", color = "cod_region", barmode = "group")

# Diseñando la app
app.layout = html.Div(
    children = [
        html.H1(children = "DASH TEST"),
        html.Div(children = """Dashboard de prueba en Dash"""),
        dcc.Graph(id = "example-graph", figure = fig)
    ]
)

if __name__ == '__main__':
    app.run_server(debug = True, port = 8050)