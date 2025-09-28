# Copyright (c) [2025]
# [Pedro Mendoza]
# []


from fastapi.responses import FileResponse
from tropycal import realtime
from fastapi import FastAPI
import datetime
import json
import os


app = FastAPI()


# Funciones ------------------------------------------------------------------

def datetimestring():
	now = datetime.datetime.now()
	return now.strftime("%Y_%m_%d")


def data_diccionario(data_storm):
    dic_data_storm = {
        "id": data_storm["id"],
        "name": data_storm["name"],
        "start_date": str(data_storm["time"][0]),
        "end_date": str(data_storm["time"][-1]),
        "max_wind": int(max(data_storm["vmax"])),
        "min_mslp": int(min(data_storm["mslp"]))}
    return dic_data_storm


# Rutas ------------------------------------------------------------------

@app.get("/")
def get_storms():
    fecha = datetimestring()
    dir = os.path.join("data", "json", fecha, "Tormentas")
    os.makedirs(dir, exist_ok=True)
    filename = f"data_tormentas.json"
    filepath = os.path.join(dir, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as archivo:
            data_storm = json.load(archivo)
        return {"Info Tormentas": data_storm}


    realtime_obj = realtime.Realtime()
    lista_tormentas = realtime_obj.list_active_storms()
    tormentas = {"Info Tormentas": lista_tormentas}

    with open(filepath, "w") as archivo:
        json.dump(tormentas, archivo, indent=3, default=str)

    return {"storm": tormentas}


@app.get("/data/{storm_name}")
def get_data(storm_name: str):
    fecha = datetimestring()

    dir = os.path.join("data", "json", fecha, storm_name)
    os.makedirs(dir, exist_ok=True)
    
    filename = f"data_{storm_name}.json"
    filepath = os.path.join(dir, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as archivo:
            data_storm = json.load(archivo)
            data_storm = data_diccionario(data_storm)
        return {"Info Tormenta": data_storm}

    realtime_obj = realtime.Realtime()
    storm = realtime_obj.get_storm(storm_name)
    tormenta = storm.to_dict()
    data_storm = data_diccionario(tormenta)

    with open(filepath, "w") as archivo:
        json.dump(tormenta, archivo, indent=3, default=str)

    return {"Info Tormenta": data_storm}


@app.get("/tormentas/")
def get_all_storms():
    path = os.path.join("storms", "summary.png")

    if not os.path.exists(path):
        realtime_obj = realtime.Realtime()
        realtime_obj.plot_summary(save_path=path)
        return FileResponse(path, media_type="image/png")

    return FileResponse(path, media_type="image/png")


@app.get("/images/{storm_name}")
def get_storm_image(storm_name: str):
    filename = f"{storm_name}.png"
    path = os.path.join("storms", filename)

    if not os.path.exists(path):
        realtime_obj = realtime.Realtime()
        storm = realtime_obj.get_storm(storm_name)
        storm.plot_forecast_realtime(save_path=path)

        return FileResponse(path, media_type="image/png")

    return FileResponse(path, media_type="image/png")