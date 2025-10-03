# Copyright (c) [2025]
# [Pedro Mendoza, Bruno Goñi, Emiliano Sánchez, Valentina Tejeda]


from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from tropycal import realtime
from fastapi import FastAPI
import datetime
import folium
import json
import os

app = FastAPI()

# Funciones ------------------------------------------------------------------

def datestring():
	now = datetime.datetime.now()
	return now.strftime("%Y_%m_%d")

def timestring():
	now = datetime.datetime.now()
	return now.strftime("%H_%M")

def calcular_rango_hora(hora):
	if hora >= 6 and hora <= 305: return "00_00"
	elif hora >= 306 and hora <= 605: return "03_00"
	elif hora >= 606 and hora <= 905: return "06_00"
	elif hora >= 906 and hora <= 1205: return "09_00"
	elif hora >= 1206 and hora <= 1505: return "12_00"
	elif hora >= 1506 and hora <= 1805: return "15_00"
	elif hora >= 1806 and hora <= 2105: return "18_00"
	else: return "21_00"

def data_diccionario(data_storm):
    dic_data_storm = {
        "id": data_storm["id"],
        "name": data_storm["name"],
        "start_date": str(data_storm["time"][0]),
        "end_date": str(data_storm["time"][-1]),
        "max_wind": int(max(data_storm["vmax"])),
        "min_mslp": int(min(data_storm["mslp"]))}
    return dic_data_storm

def get_color(vmax):
        if vmax < 34: return "blue" 
        elif vmax < 64: return "green"
        elif vmax < 83: return "yellow"
        elif vmax < 96: return "orange"
        elif vmax < 113: return "red"
        elif vmax < 137: return "purple"
        else: return "black"

def verificar_tormenta(storm_name, fecha):
    dir = os.path.join("data", fecha, "Tormentas")
    os.makedirs(dir, exist_ok=True)
    hora = calcular_rango_hora(int(timestring()))
    filename = f"{hora}.json"
    filepath = os.path.join(dir, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as archivo:
            data_storm = json.load(archivo)
            data_storm = data_storm["Info Tormentas"]
            if storm_name in data_storm:
                return True
            else:
                return False
    
    realtime_obj = realtime.Realtime()
    lista_tormentas = realtime_obj.list_active_storms()
    tormentas = {"Info Tormentas": lista_tormentas}
    with open(filepath, "w") as archivo:
        json.dump(tormentas, archivo, indent=3, default=str)
    
    if storm_name in data_storm:
        return True
    return False


# Rutas de tormentas totales ------------------------------------------------------------------

@app.get("/data")
def get_storms():
    fecha = datestring()
    dir = os.path.join("data", fecha, "Tormentas")
    os.makedirs(dir, exist_ok=True)
    hora = calcular_rango_hora(int(timestring()))
    filename = f"{hora}.json"
    filepath = os.path.join(dir, filename)

    if os.path.exists(filepath):
        with open(filepath, "r") as archivo:
            data_storm = json.load(archivo)
        return data_storm

    realtime_obj = realtime.Realtime()
    lista_tormentas = realtime_obj.list_active_storms()
    tormentas = {"Info Tormentas": lista_tormentas}

    with open(filepath, "w") as archivo:
        json.dump(tormentas, archivo, indent=3, default=str)

    return (tormentas)


@app.get("/images/tormentas")
def get_all_storms():
    fecha = datestring()
    dir = os.path.join("data", fecha, "Tormentas")
    os.makedirs(dir, exist_ok=True)
    hora = calcular_rango_hora(int(timestring()))
    filename = f"{hora}.png"
    filepath = os.path.join(dir, filename)

    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="image/png")

    realtime_obj = realtime.Realtime()
    realtime_obj.plot_summary(save_path=filepath)

    return FileResponse(filepath, media_type="image/png")

# Rutas de tormentas especificas ------------------------------------------------------------------

@app.get("/data/{storm_name}")
def get_data(storm_name: str):
    fecha = datestring()
    if not verificar_tormenta(storm_name, fecha):
        return PlainTextResponse(
            content=f"No existe tormenta con el nombre {storm_name}",
            status_code=404)


    dir = os.path.join("data", fecha, storm_name)
    os.makedirs(dir, exist_ok=True)
    hora = calcular_rango_hora(int(timestring()))
    filename = f"{hora}.json"
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


@app.get("/images/{storm_name}")
def get_storm_image(storm_name: str):
    fecha = datestring()
    if not verificar_tormenta(storm_name, fecha):
        return PlainTextResponse(
            content=f"No existe tormenta con el nombre {storm_name}",
            status_code=404)
    
    dir = os.path.join("data", fecha, storm_name)
    os.makedirs(dir, exist_ok=True)
    hora = calcular_rango_hora(int(timestring()))
    filename = f"{hora}.png"
    filepath = os.path.join(dir, filename)

    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="image/png")

    realtime_obj = realtime.Realtime()
    storm = realtime_obj.get_storm(storm_name)
    storm.plot_forecast_realtime(save_path=filepath)

    return FileResponse(filepath, media_type="image/png")


@app.get("/dynamic/{storm_name}")
def prueba(storm_name: str):
    fecha = datestring()
    if not verificar_tormenta(storm_name, fecha):
        return PlainTextResponse(
            content=f"No existe tormenta con el nombre {storm_name}",
            status_code=404)

    dir = os.path.join("data", fecha, storm_name)
    os.makedirs(dir, exist_ok=True)
    hora = calcular_rango_hora(int(timestring()))
    filename = f"{hora}.html"
    filepath = os.path.join(dir, filename)

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)

    realtime_obj = realtime.Realtime()
    storm = realtime_obj.get_storm(storm_name)
    tormenta = storm.to_dict()
    m = folium.Map(location=[tormenta["lat"][0], tormenta["lon"][0]], zoom_start=5)

    for i in range(len(tormenta["time"])):
        folium.CircleMarker(
            location=[tormenta["lat"][i], tormenta["lon"][i]],
            radius=5,
            color=get_color(tormenta["vmax"][i]),
            fill=True,
            popup=(
                f"<b>{tormenta['name']}</b><br>"
                f"Fecha: {tormenta['time'][i]}<br>"
                f"Viento: {tormenta['vmax'][i]} kt<br>"
                f"Presión: {tormenta['mslp'][i]} hPa"
            )
        ).add_to(m)

    coords = list(zip(tormenta["lat"], tormenta["lon"]))
    folium.PolyLine(coords, color="gray", weight=2.5, opacity=0.7).add_to(m)

    m.save(filepath)
    with open(filepath, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content, status_code=200)
