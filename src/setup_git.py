# Este módulo tiene la función que obtiene los datos desde GitHub (https://github.com/MinCiencia/Datos-COVID19.git)

def git_retrieve(url_source: str, data_folder: str, force_exec: bool = False):
    """Función para obtener los datos desde el repositorio del MinCiencia"""
    import os
    import sys
    import logging
    from git import Repo
    from datetime import datetime
    from src import helpers
    helpers.print_ts(code = 1, text = "Proceso de configuración del repo, comenzando.")
    # Configurando variables de ejecución
    base_path = os.getenv("BASE_APP_PATH")
    # Configurando la instancia root de logging
    log_fmt = "%(asctime)s - %(process)d - %(levelname)s - %(name)s::%(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    log_loc = os.path.join(base_path, "logs", "setup.log")
    json_file = "git_stat.json"
    logging.basicConfig(level = logging.DEBUG, 
                        filename = log_loc, 
                        filemode = "a", 
                        format = log_fmt, 
                        datefmt = date_fmt)
    logging.info(":::Comenzando proceso de configuración del repo:::")
    logging.info("Configurando el entorno...")
    # Definiendo variables de entorno
    git_url = url_source
    git_file = os.path.join(base_path, data_folder)
    # Determinando si la ejecución es necesaria: menos de 1 día de la última ejecución
    # no gatillará ejecución
    try:
        status, timestamp = helpers.pull_last_update(json_f = json_file, field = "status")
        if status == "error":
            logging.info("Se ejecutará el proceso setup_git.py.")
        else:
            if helpers.check_timediff(timestamp) < 1 and not force_exec:
                logging.warning("No se ejecutará el proceso, se trabajará con los datos existentes.")
                helpers.print_ts(code = 2, text = "No se ejecutará el proceso, se trabajará con los datos existentes.")
                return None
            else:
                logging.info("Se ejecutará el proceso setup_git.py")
    except:
        logging.warning("Se ejecutará por primera vez el proceso setup_git.py")
        logging.exception("Detalles:")
    # Revisando carpeta para dejar los archivos desde repo GitHub
    try:
        logging.info("Revisando que exista la carpeta de destino para el repo...")
        helpers.check_file(git_file)
        logging.info("La carpeta existe.")
    except:
        logging.warning("La carpeta no existe.")
        logging.exception("Detalle del error:")
        logging.info("Creando carpeta de datos...")
        os.mkdir(git_file)
        logging.info("Carpeta de datos creada.")
    # Revisando el estado del repo GitHub
    logging.info("Origen de datos definido en '{0}'".format(git_url))
    try:
        logging.info("Revisando URL del origen de datos...")
        helpers.check_url(git_url)
        logging.info("La URL responde de manera correcta (HTTP 200).")
    except:
        logging.error("La URL no responde de buena manera.")
        logging.exception("Detalle del error:")
        helpers.print_ts(code = 3, text = "La URL no responde de buena manera.")
        logging.error("Saliendo del programa, con estado 8.")
        # Escribiendo JSON de estado: error con salida 8
        current = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        status_dict = dict(status = "error", ts = current, exit_code = 8, desc = "Bad repo URL")
        helpers.print_last_update(data_dict = status_dict, json_f = json_file)
        # Salida, codigo 8
        raise Exception("El repositorio no responde. Saliendo con excepcion 8...")
    # Clonando el repo, si es que no ha sido clonado aún
    cloned = False
    try:
        logging.info("Clonando el repositorio de datos...")
        Repo.clone_from(git_url, git_file)
    except:
        logging.error("Error en el clonado.")
        logging.exception("Detalle del error:")
        cloned = True
    # Refrescando los datos, si es que el repo fue clonado
    try:
        if cloned:
            logging.info("Refrescando los datos...")
            Repo(git_file).remotes.origin.pull()
            logging.info("Datos refrescados.")
        else:
            pass
    except:
        logging.error("Error refrescando los datos.")
        logging.exception("Detalle del error:")
        logging.error("Saliendo del programa, con estado 10.")
        helpers.print_ts(code = 3, text = "Error refrescando los datos.")
        # Escribiendo JSON de estado: error con salida 8
        current = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        status_dict = dict(status = "error", ts = current, exit_code = 10, desc = "Git pull error")
        helpers.print_last_update(data_dict = status_dict, json_f = json_file)
        # Salida, codigo 10
        raise Exception("Error refrescando los datos. Saliendo con excepcion 10...")
    # Fin del proceso
    logging.info(">>>Proceso de configuración del repo, completado exitosamente.")
    helpers.print_ts(code = 1, text = "Proceso de configuración del repo, completado exitosamente.")
    # Escribiendo JSON de estado: salida 0
    current = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    status_dict = dict(status = "done", ts = current, exit_code = 0)
    helpers.print_last_update(data_dict = status_dict, json_f = json_file)
    logging.shutdown()
    return None