# Este módulo realiza el ETL necesario para tener la data

import os
import numpy as np
import pandas as pd
from src import helpers
# Configurando ejecución
base_path = os.getenv("BASE_APP_PATH")
csv_loc = os.path.join(base_path, "data", "data.csv")
# Leyendo datos en Pandas
df = pd.read_csv(csv_loc)
df.dropna(inplace = True, axis = 0, subset = ["cod_comuna"])
