#!/usr/local/bin/python
# Shell de configuración del proyecto

def main_function():
    import pdb
    # Importo los modulos de app/src
    from src import setup_env as se
    from src import setup_git as sg
    from src import setup_data as sd
    from src import setup_etl as st
    # Configurando variables de ejecución
    url_git = "https://github.com/MinCiencia/Datos-COVID19.git"
    dir_git = "git_data"
    dir_data = "data"
    # pdb.set_trace()
    print("Configurando entorno de ejecución...", flush = True)
    se.set_environment()
    print("Obteniendo datos desde GitHub...", flush = True)
    sg.git_retrieve(url_source = url_git, data_folder = dir_git)
    print("Moviendo datos a su ubicación final...", flush = True)
    sd.pull_data(data_folder = dir_git, data_prod = dir_data)
    print("Proceso finalizado.", flush = True)

if __name__ == "__main__":
    main_function()
else:
    pass