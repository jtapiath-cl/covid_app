# Este módulo contiene funciones chicas y tontas, sólo para apoyar la ejecución

def print_ts(code: int, text: str):
    import subprocess
    from datetime import datetime
    codes_dict = {1: "INFO", 2: "WARN", 3: "ERROR"}
    current_ts = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    user_print = subprocess.check_output(["whoami"]).decode("utf-8").split("\n")[0]
    output_string = "[ {0} - {1} ({2}) ]".format(codes_dict.get(code), current_ts, user_print)
    print("{0}  {1}".format(output_string, text), flush = True)
    return None

def check_url(url: str):
    import requests
    check = requests.get(url)
    if check.status_code:
        return None
    else:
        raise Exception("La URL entregada, {0}, no resuelve con estado HTTP 200.".format(url))

def check_file(work_dir: str):
    import os
    check = os.path.exists(work_dir)
    if check:
        return None
    else:
        raise Exception("El archivo o carpeta solicitado, {0}, no existe.".format(work_dir))

def check_timediff(date_base: str):
    from datetime import datetime
    ts_fmt = "%Y-%m-%d %H:%M:%S"
    ts_base = datetime.strptime(date_base, ts_fmt)
    ts_comp = datetime.now()
    tdelta = ts_comp - ts_base
    return tdelta.days

def print_last_update(data_dict: dict, json_f: str):
    import os
    import json
    json_loc = os.path.join("/app", "logs", json_f)
    with open(json_loc, "w") as json_file:
        json.dump(data_dict, json_file)
    return None

def pull_last_update(json_f: str, field: str):
    import os
    import json
    json_loc = os.path.join("/app", "logs", json_f)
    with open(json_loc) as json_file:
        data = json.load(json_file)
        # print(data)
        return data[field], data["ts"]