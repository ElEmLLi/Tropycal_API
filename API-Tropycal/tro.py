# Copyright (c) 2025
# [Pedro Mendoza, Bruno Goñi, Emiliano Sánchez, Valentina Tejeda, Brisa León]

from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, StreamingResponse
from zoneinfo import ZoneInfo as zi
from tropycal import realtime
from fastapi import FastAPI
import logging as log
import datetime as dt
from PIL import Image
import math as mt
import zipfile
import folium
import glob
import json
import os
import io

from fastapi.middleware.cors import CORSMiddleware

if not os.path.exists('logs'): os.makedirs('logs')
log.basicConfig(filename="logs\\Tropycal_API.log", level=log.INFO, format='%(levelname)s: [%(asctime)s] %(message)s')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    #"http://10.0.2.2:5173",
    "http://localhost:5173",
    #"http://192.168.1.45:5173"
    ],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Funciones ------------------------------------------------------------------

KEY_TRANSLATIONS = {
    "id": "id",
    "operational_id": "id_operacional",
    "name": "nombre",
    "year": "año",
    "season": "temporada",
    "basin": "cuenca",
    "source_info": "informacion_fuente",
    "realtime": "tiempo_real",
    "invest": "investigacion",
    "source_method": "metodo_fuente",
    "source_url": "url_fuente",
    "source": "origen",
    "jtwc_source": "fuente_jtwc",
    "time": "tiempo",
    "extra_obs": "observaciones_extra",
    "special": "especial",
    "type": "tipo",
    "lat": "latitud",
    "lon": "longitud",
    "vmax": "vmax",
    "mslp": "mslp",
    "wmo_basin": "cuenca_wmo",
    "ace": "ace",
    "prob_2day": "prob_2dias",
    "prob_7day": "prob_7dias",
    "risk_2day": "riesgo_2dias",
    "risk_7day": "riesgo_7dias",
    "fecha_hora de captura": "fecha_hora_captura",
    "zona horaria de captura": "zona_horaria_captura",
}

def translate_key(key: str) -> str:
    return KEY_TRANSLATIONS.get(key, key)

def translate_json(data):
    if isinstance(data, dict):
        return {translate_key(k): translate_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [translate_json(item) for item in data]
    else:
        return data

def datestring():
	now = dt.datetime.now()
	return now.strftime("%Y_%m_%d")

def timestring():
	now = dt.datetime.now()
	return now.strftime("%H_%M")

def datajsonextra():
    utc_now = dt.datetime.now(zi("UTC"))
    mexico_tz = zi("America/Mexico_City")
    mexico_time = utc_now.astimezone(mexico_tz)
    print(mexico_time)
    return mexico_time, mexico_tz

def CrearMsgLog(status_code, ruta, msg) :
    return f"GET /{ruta} HTTP/1.1 {status_code} [{msg}]"

def errornan(lista):
    lst = []
    for i in lista: 
        if not mt.isnan(i) == True: lst.append(i)
    return int(min(lst))

def listaTormentasCompleta(listaActual, listaNueva): 
    for storm in listaNueva: 
        if not storm in listaActual: listaActual.append(storm)
    return listaActual

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
        "lon": str(data_storm["lon"][-1]),
        "lat": str(data_storm["lat"][-1]),
        "basin": str(data_storm["wmo_basin"][-1]),
        "max_wind": int(max(data_storm["vmax"])),
        "min_mslp": errornan(data_storm["mslp"])}
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
    mexico_time, mexico_tz = datajsonextra()
    tormentas["fecha_hora de captura"] = mexico_time
    tormentas["zona horaria de captura"] = mexico_tz

    with open(filepath, "w") as archivo:
        json.dump(tormentas, archivo, indent=3, default=str)
    
    if storm_name in data_storm:
        return True
    return False

# Rutas de origen ----------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {"Welcome to Tropycal API"}

# Rutas de tormentas totales ------------------------------------------------------------------

@app.get("/data")
def get_storms():
    try:
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
        mexico_time, mexico_tz = datajsonextra()
        tormentas["fecha_hora de captura"] = mexico_time
        tormentas["zona horaria de captura"] = mexico_tz

        with open(filepath, "w") as archivo:
            json.dump(tormentas, archivo, indent=3, default=str)
        
        with open(filepath, "r") as archivo:
            data_storm = json.load(archivo)
        return data_storm

    except Exception as exc:
        log.error(CrearMsgLog(404, f"data/", exc))
        return PlainTextResponse(content=f"Hubo un error al obtener la data", status_code=404)


@app.get("/images")
def get_all_storms_map():
    try:
        fecha = datestring()
        dir = os.path.join("data", fecha, "Tormentas")
        os.makedirs(dir, exist_ok=True)
        hora = calcular_rango_hora(int(timestring()))
        filename = f"{hora}.png"
        filepath = os.path.join(dir, filename)

        if os.path.exists(filepath):
            log.info(CrearMsgLog(200, "images", "Successful request"))
            return FileResponse(filepath, media_type="image/png")

        realtime_obj = realtime.Realtime()
        realtime_obj.plot_summary(save_path=filepath)

        log.info(CrearMsgLog(200, "images/tormentas", "Successful request"))
        return FileResponse(filepath, media_type="image/png")
    
    except Exception as exc:
        log.error(CrearMsgLog(404, "images/tormentas", exc))
        return PlainTextResponse(content=f"Hubo un error al obtener la data", status_code=500)


@app.get("/dynamic")
def dynamic_storm_map():
    try:
        fecha = datestring()
        dir = os.path.join("data", fecha, "Tormentas")
        os.makedirs(dir, exist_ok=True)

        hora = calcular_rango_hora(int(timestring()))
        html_filepath = os.path.join(dir, f"{hora}.html")
        json_filepath = os.path.join(dir, f"{hora}.json")

        if os.path.exists(html_filepath):
            with open(html_filepath, "r", encoding="utf-8") as f:
                html_content = f.read()
            log.info(CrearMsgLog(200, f"dynamic/", "Successful request"))
            return HTMLResponse(content=html_content, status_code=200)

        realtime_obj = realtime.Realtime()

        if os.path.exists(json_filepath):
            with open(json_filepath, "r") as archivo:
                tormentas = json.load(archivo)
            data_storm = tormentas["Info Tormentas"]

        else:
            lista_tormentas = realtime_obj.list_active_storms()
            mexico_time, mexico_tz = datajsonextra()

            tormentas = {
                "Info Tormentas": lista_tormentas,
                "fecha_hora de captura": mexico_time,
                "zona horaria de captura": mexico_tz
            }
            data_storm = lista_tormentas

            with open(json_filepath, "w") as archivo:
                json.dump(tormentas, archivo, indent=3, default=str)

        map = folium.Map(location=[19.5, 99.4], zoom_start=5)

        if len(data_storm) == 0:
            log.info(CrearMsgLog(200, f"dynamic/", "Solicitud sin tormentas activas"))
            return PlainTextResponse(content=f"No hay tormentas activas", status_code=404)

        for id_storm in data_storm:
            storm = realtime_obj.get_storm(id_storm)
            tormenta = storm.to_dict()

            coords_hist = list(zip(tormenta["lat"], tormenta["lon"]))
            folium.PolyLine(coords_hist, color="gray", weight=2.5, opacity=0.7).add_to(map)

            for i in range(len(tormenta["time"])):
                folium.CircleMarker(
                    location=[tormenta["lat"][i], tormenta["lon"][i]],
                    radius=5,
                    color=get_color(tormenta["vmax"][i]),
                    fill=True,
                    popup=f"<b>{tormenta['name']}</b><br>Fecha: {tormenta['time'][i]}<br>Viento: {tormenta['vmax'][i]} kt<br>Presión: {tormenta['mslp'][i]} hPa"
                ).add_to(map)

            folium.Marker(
                location=[tormenta["lat"][-1], tormenta["lon"][-1]],
                popup="Ubicación actual de la tormenta"
            ).add_to(map)

            pred = storm.get_forecast_realtime()
            coords_pred = list(zip(pred["lat"], pred["lon"]))
            folium.PolyLine(coords_pred, color="red", weight=2.5, opacity=0.7, dash_array='3, 3').add_to(map)

            for i in range(len(pred["fhr"])):
                folium.CircleMarker(
                    location=[pred["lat"][i], pred["lon"][i]],
                    radius=5,
                    color=get_color(pred["vmax"][i]),
                    fill=True,
                    popup=f"<b>{tormenta['name']} - Predicción</b><br>+{pred['fhr'][i]}h<br>Viento: {pred['vmax'][i]} kt"
                ).add_to(map)

        map.save(html_filepath)

        with open(html_filepath, "r", encoding="utf-8") as f:
            html_content = f.read()

        log.info(CrearMsgLog(200, f"dynamic/", "Successful request"))
        return HTMLResponse(content=html_content, status_code=200)

    except Exception as exc:
        log.error(CrearMsgLog(404, f"dynamic/", exc))
        return PlainTextResponse(content=f"Hubo un error al obtener la data", status_code=500)

# Rutas de tormentas especificas ------------------------------------------------------------------

@app.get("/data/{storm_name}")
def get_data_storm(storm_name: str):
    try:
        fecha = datestring()
        if not verificar_tormenta(storm_name, fecha):
            log.info(CrearMsgLog(200, f"data/{storm_name}", f"No existe tormenta con el nombre {storm_name}"))
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

            log.info(CrearMsgLog(200, f"data/{storm_name}", "Successful request"))
            return data_storm

        realtime_obj = realtime.Realtime()
        storm = realtime_obj.get_storm(storm_name)
        mexico_time, mexico_tz = datajsonextra()
        tormenta = storm.to_dict()
        tormenta["fecha_hora de captura"] = mexico_time
        tormenta["zona horaria de captura"] = mexico_tz
        data_storm = data_diccionario(tormenta)

        with open(filepath, "w") as archivo:
            json.dump(tormenta, archivo, indent=3, default=str)

        log.info(CrearMsgLog(200, f"data/{storm_name}", "Successful request"))
        return data_storm
    
    except Exception as exc:
        log.error(CrearMsgLog(404, f"data/{storm_name}", exc))
        return PlainTextResponse(content=f"Hubo un error al obtener la data", status_code=500)

@app.get("/images/{storm_name}")
def get_storm_map_image(storm_name: str):
    try:
        fecha = datestring()
        if not verificar_tormenta(storm_name, fecha):
            log.info(CrearMsgLog(200, f"images/{storm_name}", f"No existe tormenta con el nombre {storm_name}"))
            return PlainTextResponse(
                content=f"No existe tormenta con el nombre {storm_name}",
                status_code=404)
        
        dir = os.path.join("data", fecha, storm_name)
        os.makedirs(dir, exist_ok=True)
        hora = calcular_rango_hora(int(timestring()))
        filename = f"{hora}.png"
        filepath = os.path.join(dir, filename)

        if os.path.exists(filepath):
            log.info(CrearMsgLog(200, f"images/{storm_name}", "Successful request"))
            return FileResponse(filepath, media_type="image/png")

        realtime_obj = realtime.Realtime()
        storm = realtime_obj.get_storm(storm_name)
            
        storm.plot_forecast_realtime(save_path=filepath)

        log.info(CrearMsgLog(200, f"images/{storm_name}", "Successful request"))
        return FileResponse(filepath, media_type="image/png")
    
    except Exception as exc:
        log.error(CrearMsgLog(404, f"images/{storm_name}", exc))
        return PlainTextResponse(content=f"Hubo un error al obtener la data", status_code=500)



@app.get("/dynamic/{storm_name}")
def dynamic_strom_name_map(storm_name: str):
    try:
        fecha = datestring()
        if not verificar_tormenta(storm_name, fecha):
            log.info(CrearMsgLog(200, f"dynamic/{storm_name}", f"No existe tormenta con el nombre {storm_name}"))
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
            log.info(CrearMsgLog(200, f"dynamic/{storm_name}", "Successful request"))
            return HTMLResponse(content=html_content, status_code=200)

        realtime_obj = realtime.Realtime()
        storm = realtime_obj.get_storm(storm_name)
        tormenta = storm.to_dict()
        map = folium.Map(location=[tormenta["lat"][0], tormenta["lon"][0]], zoom_start=5)

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
            ).add_to(map)

        coords = list(zip(tormenta["lat"], tormenta["lon"]))
        folium.PolyLine(coords, color="gray", weight=2.5, opacity=0.7).add_to(map)

        folium.Marker(location=[tormenta["lat"][-1], tormenta["lon"][-1]], 
                      popup=folium.Popup("Ubicacion actual de la tormenta", parse_html=True, max_width=100)
        ).add_to(map)

        prediccion_tormenta = storm.get_forecast_realtime()

        for i in range(len(prediccion_tormenta["fhr"])):
            folium.CircleMarker(
                location=[prediccion_tormenta["lat"][i], prediccion_tormenta["lon"][i]],
                radius=5,
                color=get_color(prediccion_tormenta["vmax"][i]),
                fill=True,
                dashArray='3, 3',
                popup=(
                    f"<b>{tormenta['name']} - Prediccion</b><br>"
                    f"Proximas: {prediccion_tormenta['fhr'][i]} horas<br>"
                    f"Viento: {prediccion_tormenta['vmax'][i]} kt<br>"
                    f"Presión: {prediccion_tormenta['mslp'][i]} hPa"
                )
            ).add_to(map)

        coords = list(zip(prediccion_tormenta["lat"], prediccion_tormenta["lon"]))
        folium.PolyLine(coords, color="red", weight=2.5, opacity=0.7, dashArray='3, 3',).add_to(map)

        map.save(filepath)
        with open(filepath, "r", encoding="utf-8") as file:
            html_content = file.read()

        log.info(CrearMsgLog(200, f"dynamic/{storm_name}", "Successful request"))
        return HTMLResponse(content=html_content, status_code=200)
    
    except Exception as exc:
        log.error(CrearMsgLog(404, f"dynamic/{storm_name}", exc))
        return PlainTextResponse(content=f"Hubo un error al obtener la data", status_code=500)


# Rutas por solicitud de fecha ----------------------------------------------------------------------------------

@app.get("/data_date/{date}")
def data_date_storm(date: str):
    try:
        HourNames = ["00_00", "03_00", "06_00", "09_00", "12_00", "15_00", "18_00", "21_00"]
        StormsLst = []
        for hour in HourNames:
            filepath = os.path.join("data", date, "Tormentas", hour + ".json")

            if os.path.exists(filepath):
                with open(filepath, "r") as archivo:
                    data_storm = json.load(archivo)
                    infStorms = data_storm.get("Info Tormentas", [])
                    StormsLst = listaTormentasCompleta(StormsLst, infStorms)

        if len(StormsLst) == 0: 
            log.info(CrearMsgLog(200, f"data_date/{date}", f"Sin informacion de tormentas el {date}"))
            return PlainTextResponse(content=f"No tengo registro de tormentas el {date}", status_code=404)
        
        response_data = {"Info Tormentas": StormsLst}

        log.info(CrearMsgLog(200, f"data_date/{date}", "Successful request"))
        return response_data

    except Exception as exc:
        log.error(CrearMsgLog(500, f"data_date/{date}", exc))
        return PlainTextResponse(content="Error al obtener la data", status_code=500)

@app.get("/hour_date/{date}/{storm_name}")
def hour_date_storm(date: str, storm_name: str):
    try:
        HourNames = ["00_00", "03_00", "06_00", "09_00", "12_00", "15_00", "18_00", "21_00"]
        hours_found = []

        for hour in HourNames:
            file_path = os.path.join("data", date, storm_name, hour + ".json")
            if os.path.exists(file_path):
                hours_found.append(hour)

        if len(hours_found) == 0:
            log.info(CrearMsgLog(404, f"/hour_date/{date}/{storm_name}", "Sin informacion de horas registradas"))
            return hours_found

        log.info(CrearMsgLog(200, f"/hour_date/{date}/{storm_name}", "Horas encontradas"))
        return hours_found

    except Exception as exc:
        log.error(CrearMsgLog(500, f"/hour_date/{date}/{storm_name}", exc))
        return PlainTextResponse(content=f"Error al obtener las horas", status_code=500)

@app.get("/data_date/{date}/{storm_name}/{hour}")
def data_date_storm(date: str, storm_name: str, hour: str):
    try:
        dir = os.path.join("data", date, storm_name, hour + ".json")

        if os.path.exists(dir):
            with open(dir, "r") as archivo:
                data_storm = json.load(archivo)
                data_storm = data_diccionario(data_storm)

            log.info(CrearMsgLog(200, f"/data_date/{date}/{storm_name}/{hour}", "Successful request"))
            return data_storm
        
        log.info(CrearMsgLog(200, f"/data_date/{date}/{storm_name}/{hour}", f"Sin informacion de tormenta {storm_name} el {date}"))
        return PlainTextResponse(content=f"No tengo registro de tormenta {storm_name} el {date}", status_code=404)

    except Exception as exc:
        log.error(CrearMsgLog(404, f"data_date/{date}/{storm_name}/{hour}", exc))
        return PlainTextResponse(content=f"Error al obtener la data", status_code=500)
    

@app.get("/image_date/{date}/{storm_name}/{hour}")
def image_date(date: str, storm_name: str, hour: str):
    # Ruta correcta al archivo .png
    base_dir = os.path.join("data", date, storm_name, f"{hour}.png")

    # Verificar si el archivo existe
    if os.path.exists(base_dir):
        log.info(CrearMsgLog(200, f"image_date/{date}/{storm_name}", "Successful request - Imagen encontrada"))
        return FileResponse(base_dir, media_type="image/png")

    log.info(
        CrearMsgLog(
            404,
            f"image_date/{date}/{storm_name}",
            f"Sin imágenes para {storm_name} en {date} (hora {hour})"
        )
    )

    return PlainTextResponse(
        content=f"No tengo registro de tormenta {storm_name} el {date} en la hora {hour}",
        status_code=404
    )


@app.get("/data_forecast/{date}/{storm_name}/{hour}")
def get_data_storm(date: str, storm_name: str, hour: str):
    try:
        base_dir = os.path.join("data", date, storm_name, f"{hour}_forecast.json")

        if os.path.exists(base_dir):
            with open(base_dir, "r") as archivo:
                data_storm = json.load(archivo)

            log.info(CrearMsgLog(200, f"/data_forecast/{date}/{storm_name}/{hour}", "Successful request"))
            return data_storm

        return PlainTextResponse(content=f"No tengo registro de tormenta {storm_name} el {date}", status_code=404)
        
    except Exception as exc:
        log.error(CrearMsgLog(500, f"data_forecast/{storm_name}", str(exc)))
        return PlainTextResponse(content="Hubo un error al obtener la data de forecast", status_code=500)


@app.get("/TraducirJson/{date}/{storm_name}/{hour}")
def traducir_json(date: str, storm_name: str, hour: str):

    # Ruta del archivo JSON
    json_path = os.path.join("data", date, storm_name, hour + ".json")

    # Verificación
    if not os.path.exists(json_path):
        return PlainTextResponse(content=f"No pude traducir el json {json_path}", status_code=404)

    # Leer el archivo JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Traducir claves
    data_traducida = translate_json(data)

    return data_traducida


@app.get("/zipTormenta/{date}/{storm_name}")
def zip_tormenta(date: str, storm_name: str):

    carpeta_a_comprimir = os.path.join("data", date, storm_name)

    # Verificar que la carpeta existe
    if not os.path.isdir(carpeta_a_comprimir):
        raise PlainTextResponse(status_code=404, content="Carpeta no encontrada")

    # Crear buffer en memoria
    zip_buffer = io.BytesIO()

    # Crear ZIP dentro del buffer
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(carpeta_a_comprimir):
            for file in files:
                ruta_completa = os.path.join(root, file)
                ruta_relativa = os.path.relpath(ruta_completa, carpeta_a_comprimir)
                zipf.write(ruta_completa, ruta_relativa)

    # Mover puntero al inicio del buffer
    zip_buffer.seek(0)

    # Devolver como archivo descargable
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename={storm_name}_{date}.zip"
        }
    )