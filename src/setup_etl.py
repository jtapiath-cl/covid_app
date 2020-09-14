# Este módulo realiza el ETL necesario para tener la data

def data_etl():
    import os
    import logging
    import numpy as np
    import pandas as pd
    import pandasql as ps
    # Configurando ejecución
    base_path = os.getenv("BASE_APP_PATH")
    csv_loc = os.path.join(base_path, "data", "data.csv")
    # Configurando la instancia root de logging
    log_fmt = "%(asctime)s - %(process)d - %(levelname)s - %(name)s::%(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    log_loc = os.path.join(base_path, "logs", "setup.log")
    # Configurando logging
    logging.basicConfig(level = logging.DEBUG, 
                        filename = log_loc, 
                        filemode = "a", 
                        format = log_fmt, 
                        datefmt = date_fmt)
    logging.info(":::Comenzando proceso de lectura de la data:::")
    logging.info("Leyendo datos...")
    # Leyendo datos en Pandas
    df = pd.read_csv(csv_loc)
    logging.info("Transformando datos...")
    df["fecha"] = pd.to_datetime(df["fecha"], format = "%Y-%m-%d")
    logging.info("Obteniendo valores únicos de regiones...")
    df_reg_tmp = ps.sqldf("SELECT DISTINCT region, cod_region FROM df")
    regiones = df_reg_tmp.to_dict(orient = "records")
    logging.info("Obteniendo valores únicos de comunas...")
    df_com_tmp = ps.sqldf("SELECT DISTINCT comuna, cod_comuna FROM df")
    comunas = df_com_tmp.to_dict(orient = "records")
    logging.info("Retornando datos...")
    logging.info(">>>Proceso de lectura de la data, completado exitosamente.")
    return df, regiones, comunas