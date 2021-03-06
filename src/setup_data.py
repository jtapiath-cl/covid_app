# Este módulo tiene la función que toma los datos desde GitHub y los lleva a la carpeta app/data

def pull_data(data_folder: str, data_prod: str, force_exec: bool = False):
    """Función para tomar los datos desde el repo GitHub y dejarlos en la
    ubicación de producción."""
    import os
    import pdb
    import sys
    import shutil 
    import logging
    import numpy as np
    import pandas as pd
    from datetime import datetime
    from src import helpers
    # pdb.set_trace()
    helpers.print_ts(code = 1, text = "Proceso de configuración de la data, comenzando.")
    # Configurando variables de ejecución
    base_path = os.getenv("BASE_APP_PATH")
    # Configurando la instancia root de logging
    log_fmt = "%(asctime)s - %(process)d - %(levelname)s - %(name)s::%(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    log_loc = os.path.join(base_path, "logs", "setup.log")
    json_file = "data_stat.json"
    # Configurando logging
    logging.basicConfig(level = logging.DEBUG, 
                        filename = log_loc, 
                        filemode = "a", 
                        format = log_fmt, 
                        datefmt = date_fmt)
    logging.info(":::Comenzando proceso de configuración de la data:::")
    logging.info("Configurando el entorno...")
    # Definiendo variables de entorno
    git_file = os.path.join(base_path, data_folder)
    csv_fold = os.path.join(base_path, data_prod)
    csv_file = os.path.join(base_path, data_prod, "Covid-19_std.csv")
    data_src = os.path.join(git_file, "output", "producto1", "Covid-19_std.csv")
    data_fnl = os.path.join(base_path, data_prod, "data.csv")
    previous_folder = False
    perform_load = True
    # Revisando si existe el archivo de datos a manipular
    try:
        logging.info("Revisando que exista el archivo con los datos a utilizar...")
        helpers.check_file(data_src)
        logging.info("El archivo existe.")
    except:
        logging.error("El archivo de datos no existe.")
        logging.exception("Detalle del error:")
        helpers.print_ts(code = 3, text = "Los datos aún no son descargados.")
        logging.error("Saliendo del programa, con estado 5.")
        # Escribiendo JSON de estado: 
        current = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        status_dict = dict(status = "error", ts = current, exit_code = 5, 
                            desc_stat = "No available data", last_date = None)
        helpers.print_last_update(data_dict = status_dict, json_f = json_file)
        raise Exception("El archivo de datos no existe. Saliendo con excepcion 5...")
    # Revisando si existe la carpeta objetivo
    try:
        logging.info("Revisando que exista la carpeta de destino para la data...")
        helpers.check_file(csv_fold)
        logging.info("La carpeta existe.")
        previous_folder = True
    except:
        logging.warning("La carpeta no existe.")
        logging.exception("Detalle del error:")
        logging.info("Creando carpeta de datos...")
        os.mkdir(csv_fold)
        logging.info("Carpeta de datos creada.")
    # Leyendo el archivo a un dataframe de Pandas
    logging.info("Leyendo datos recién cargados...")
    df_tmp = pd.read_csv(data_src)
    last_dt = max(df_tmp.Fecha)
    try:
        logging.info("Leyendo datos de la última corrida exitosa...")
        df_tmp_2 = pd.read_csv(data_fnl)
        logging.info("Datos leidos.")
        previous_folder = True
        if force_exec:
            pass
        else:
            perform_load = False
    except:
        df_tmp_2 = None
        logging.error("No hay datos previos.")
        logging.exception("Detalles del error:")
        logging.info("Se ejecutará el proceso de configuracion setup_data.py")
    # Si la última fecha disponible es mayor a la última fecha guardada, se copia a la nueva ubicación
    if perform_load:
        pass
    else:
        logging.info("Obteniendo fechas a comparar: última carga, últimos guardados, último registro...")
        try:
            saved_dt = max(df_tmp_2.fecha)
            saved_dt_json = helpers.pull_last_update(json_f = json_file, field = "last_date")[0]
            logging.info("La última ejecución obtuvo datos del día {0}".format(last_dt))
            logging.info("Los últimos datos guardados son del día {0}".format(saved_dt))
            logging.info("La última ejecución tiene registro de la fecha {0}".format(saved_dt_json))
            del df_tmp, df_tmp_2
        except:
            logging.error("Uno o más de los archivos fuente no existe.")
            logging.exception("Detalles del error:")
            logging.info("Se ejecutará el proceso de configuración setup_data.py")
            perform_load = True
        try:
            logging.info("Revisando que las fechas coincidan para la ultima ejecucion guardada...")
            if saved_dt == saved_dt_json:
                logging.info("Las fechas coinciden.")
            else:
                raise Exception("Las fechas guardadas del ultimo proceso de carga no coinciden.")
        except:
            logging.error("Las fechas almacenadas de la ultima ejecucion del proceso no coinciden.")
            logging.exception("Detalle del error:")
            logging.info("Se ejecutará el proceso de configuracion setup_data.py")
            perform_load = True
        # Se revisan las fechas procesadas para verificar que se debe ejecutar el proceso o se mantiene la fecha anterior
        try:
            if perform_load:
                pass
            else:
                logging.info("Revisando la última fecha procesada...")
                if saved_dt_json == None:
                    logging.info("La última ejecución fue errónea o no existe.")
                    raise Exception("La ultima ejecucion fue erronea o no existe.")
                else:
                    if last_dt <= saved_dt and previous_folder:
                        logging.warning("No se ejecutará el proceso, se trabajará con los datos existentes.")
                        helpers.print_ts(code = 2, text = "No se ejecutará el proceso, se trabajará con los datos existentes.")
                        return None
                    else:
                        logging.info("Se ejecutará el proceso setup_data.py")
                        perform_load = True
        except:
            logging.warning("Se ejecutará el proceso setup_data.py")
            logging.exception("Detalles del error:")
    try:
        if not perform_load and not force_exec:
            pass
        else:
            logging.info("Copiando archivo origen de datos a ubicación final...")
            shutil.copyfile(data_src, csv_file)
            logging.info("Archivo copiado.")
    except:
        logging.error("Error al copiar el archivo fuente a su ubicación final.")
        logging.exception("Detalle del error:")
        helpers.print_ts(code = 3, text = "Error al copiar el archivo fuente a su ubicación final.")
        logging.error("Saliendo del programa, con estado 15.")
        # Escribiendo JSON de estado: 
        current = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        status_dict = dict(status = "error", ts = current, exit_code = 15, 
                            last_date = None, desc_stat = "Copy error")
        helpers.print_last_update(data_dict = status_dict, json_f = json_file)
        raise Exception("Error al copiar el archivo de datos. Saliendo con excepcion 15...")
    # Transformando la data en Pandas para mejor lectura
    logging.info("Lectura de datos finales en Pandas...")
    df_final = pd.read_csv(csv_file)
    dict_cols = {"Region": "region", "Codigo region": "cod_region", "Comuna": "comuna",
                    "Codigo comuna": "cod_comuna", "Poblacion": "poblacion", "Fecha": "fecha",
                    "Casos confirmados": "casos"}
    logging.info("Cambiando nombre de columnas...")
    df_final.rename(columns = dict_cols, inplace = True)
    logging.info("Nombres de columnas cambiados.")
    logging.info("Cambiando columna 'fecha' a formato fecha...")
    try:
        logging.info("Guardando los datos finales en la ubicación de producción...")
        df_final.to_csv(data_fnl, index = False, encoding = "utf-8")
        logging.info("Datos guardados.")
    except:
        logging.error("Error al guardar el archivo de datos final.")
        logging.exception("Detalle del error:")
        helpers.print_ts(code = 3, text = "Error al guardar el archivo de datos final.")
        logging.error("Saliendo del programa, con estado 22.")
        # Escribiendo JSON de estado: 
        current = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        status_dict = dict(status = "error", ts = current, exit_code = 22, 
                            last_date = None, desc_stat = "Save error")
        helpers.print_last_update(data_dict = status_dict, json_f = json_file)
        raise Exception("El archivo de datos no se pudo guardar. Saliendo con excepcion 22...")
    # Fin del proceso
    logging.info(">>>Proceso de obtención de la data, completado exitosamente.")
    helpers.print_ts(code = 1, text = "Proceso de obtención de la data, completado exitosamente.")
    # Escribiendo JSON de estado: 
    current = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    status_dict = dict(status = "copied", ts = current, last_date = last_dt, exit_code = 0)
    helpers.print_last_update(data_dict = status_dict, json_f = json_file)
    logging.shutdown()
    return None
