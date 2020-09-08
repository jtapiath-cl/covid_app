# Este módulo realiza el ETL necesario para tener la data

def data_etl():
    import os
    import numpy as np
    import pandas as pd
    import pandasql as ps
    # Configurando ejecución
    base_path = os.getenv("BASE_APP_PATH")
    csv_loc = os.path.join(base_path, "data", "data.csv")
    # Leyendo datos en Pandas
    df = pd.read_csv(csv_loc)
    df_reg_tmp = ps.sqldf("SELECT DISTINCT region, cod_region FROM df")
    regiones = df_reg_tmp.to_dict(orient = "records")
    df_com_tmp = ps.sqldf("SELECT DISTINCT comuna, cod_comuna FROM df")
    comunas = df_com_tmp.to_dict(orient = "records")
    return df, regiones, comunas