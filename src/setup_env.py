# Este módulo configura las variables de entorno basado en el ambiente en que se ejecute

def set_environment():
    """Función para fijar variables de ambiente, como el directorio base de la app"""
    import os
    import sys
    import socket
    import logging
    from datetime import datetime
    from src import helpers as helpers
    # Obtengo el hostname de la máquina donde se está ejecutando
    helpers.print_ts(code = 1, text = "Proceso de configuración del ambiente, comenzando.")
    # Configurando la instancia root de logging
    log_fmt = "%(asctime)s - %(process)d - %(levelname)s - %(name)s::%(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    # Ubicacion del log
    log_fld = os.path.join(os.path.join(os.path.dirname(__file__), ".."), "logs")
    log_loc = os.path.join(log_fld, "setup.log")
    # Si la carpeta ../logs no existe, se crea
    try:
        helpers.check_file(log_fld)
    except:
        os.mkdir(log_fld)
    # Configurando la instancia de log
    logging.basicConfig(level = logging.DEBUG, 
                        filename = log_loc, 
                        filemode = "a", 
                        format = log_fmt, 
                        datefmt = date_fmt)
    logging.info(":::Comenzando proceso de configuración del ambiente:::")
    logging.info("Configurando el entorno...")
    # Variables de ejecución
    json_file = "env_stat.json"
    host = socket.gethostname()
    logging.info("Nombre de la máquina donde se ejecuta la app: {0}".format(host))
    # Asigno un directorio base de acuerdo al host
    logging.info("Revisando ambiente de ejecución y definiendo ruta base...")
    if host.lower()[:3] == "lap":
        # Entorno local de desarrollo
        logging.info("La app está corriendo en el entorno local de desarrollo.")
        os.environ["BASE_APP_PATH"] = "/home/jtapia/Projects/20200907-covid_app"
    elif host.lower()[:3] == "dwa":
        # Entorno remoto de desarrollo
        logging.info("La app está corriendo en el entorno remoto de desarrollo.")
        os.environ["BASE_APP_PATH"] = os.getcwd()
    elif host.lower()[:3] == "prd":
        # Entorno de producción
        logging.info("La app está corriendo en el entorno de producción.")
        os.environ["BASE_APP_PATH"] = "/app"
    else:
        logging.error("La app está corriendo en un entorno desconocido.")
        helpers.print_ts(code = 3, text = "El entorno de ejecución no es conocido.")
        logging.error("Saliendo del programa, con estado 2.")
        sys.exit(2)
    path = os.getenv("BASE_APP_PATH")
    logging.info("Ruta base de la app: {0}.".format(path))
    logging.info(">>>Proceso de configuración del amiente, completado con éxito.")
    helpers.print_ts(code = 1, text = "Proceso de configuración del ambiente, completado con éxito.")
    # Escribiendo JSON de estado: 
    current = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    status_dict = dict(status = "done", ts = current, exit_code = 0, 
                        hostname = host, path = path)
    helpers.print_last_update(data_dict = status_dict, json_f = json_file)
    logging.shutdown()
    return None
