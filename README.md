# Tropycal_API

##  Introduccion
Tropycal_API es un proyecto desarrollado en python con el objetivo de hacer una API que permita obtener datos de tormentas y huracanes obteneidos por la NHC, usando como base la libreria [Tropycal](https://tropycal.github.io/tropycal/).

## Librerias y Dependencias

```
pip install "fastapi[standard]" tropycal cartopy shapely folium pillow
```

[FastAPI](https://fastapi.tiangolo.com/#run-it)  
[Folium](https://python-visualization.github.io/folium/latest/)

## How to run 
Rcomendamos tener **Python 3.11** o superior

Ingresa a la carpeta /API-Tropycal, y en terminal ejecuta
```
uvicorn tro:app
```
[Documentacion FastAPI](https://fastapi.tiangolo.com/#run-it)

Una vez que el proyecto esté corriendo, podrás acceder a él a través de tu IP de loopback (generalmente el puerto 8000 por defecto): 

*[http://127.0.0.1:8000](http://127.0.0.1:8000)*

Puedes abrir tu host agregando
```
--host tu-IP
```

Puedes escoger el puerto agregando
```
--port [numero de puerto]
```

## Rutas y llamadas

### `"/data"`
Obtiene y retorna la lista de **tormentas activas**.

### `"/data/{storm_name}"`
Sustituye **[storm_name]** por el nombre de alguna tormenta activa.  
Esta ruta devuelve información resumida de la tormenta: **ID, nombre, fecha de inicio, fecha de finalización, viento máximo y presión mínima**, y además guarda la información completa en una carpeta local.

### `"/images/tormentas"`
Devuelve una visualización **gráfica de todas las tormentas actuales**.

### `"/images/{storm_name}"`
Sustituye **[storm_name]** por el nombre de alguna tormenta activa.  
Esta ruta devuelve una **imagen gráfica** de la tormenta y la guarda en una carpeta local.

### `"/dynamic"` 
Devuelve un **mapa interactivo** con los puntos graficados correspondientes a todas las tormentas activas.

### `"/dynamic/{storm_name}"`
Sustituye **[storm_name]** por el nombre de alguna tormenta activa.  
Devuelve un **mapa interactivo** con los puntos graficados correspondientes a la tormenta solicitada.

### `"/data_date/{date}"`
En un formato ***año_mes_dia*** para **[date]**,  te regresa la lista de tormentas que registro a la primera hora (00:00), datos otorgada por la NHC.

### `"/data_date/{date}/{storm_name}"`
En un formato ***año_mes_dia*** para **[date]**,  y el id de la tormenta para **[storm_name]**, te regresa la información de la tormenta solicitada del dia solicitado, estos de la primeraa hora (00:00) de datos otorgada por la NHC.

### `"/image_date/{date}/{storm_name}"`
En un formato ***año_mes_dia*** para **[date]**,   y el id de la tormenta para **[storm_name]**, te regresa un archivo formato gif con la trayectoria que siguio la tormenta especificada.

## Ultimas novedades 
* Incorporamos la solicitud de archivo formato gif para visualizacion animada de la tormenta

## Funcionalidades a incorporar
* Creacion de cono de incertidumbre para la prediccion
* Verificacion de formato de fecha

## Soporte 
Actualmente el proyecto se encuentra en desarrollo. Cualquier duda o sugerencia al correo especficiado de los autores