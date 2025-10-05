# Tropycal_API

##  Introduccion
Tropycal_API es un proyecto desarrollado en python con el objetivo de hacer una API que permita obtener datos de tormentas y huracanes obteneidos por la NHC, usando como base la libreria [Tropycal](https://tropycal.github.io/tropycal/).

## Librerias y Dependencias

```
pip install "fastapi[standard]" tropycal cartopy shapely folium
```

[FastAPI](https://fastapi.tiangolo.com/#run-it)  
[Folium](https://python-visualization.github.io/folium/latest/)

## How to run 
Rcomendamos tener **Python 3.11** o superior

Dentro del proyecto
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

### `"/dynamic/{storm_name}"`
Sustituye **[storm_name]** por el nombre de alguna tormenta activa.  
Devuelve un **mapa interactivo** con los puntos graficados correspondientes a la tormenta solicitada.

## Ultimas novedades 
* Hemos ajustado los path para guardar la informacion, menos redundante y mas conjunta segun la tormenta
* La hora obtenida se ajusta segun el rango de obtencion de informacion
* Se agrego la obtencion de hora para ubicar la informacion solicitada
* Hemos arreglado la busqueda de tormentas no existentes
* Incorporacion de Logs de informacion y de errores
* Solucion de manejo de errores

## Funcionalidades a incorporar
* Agregar un archivo .sh encargado de hacer la solicitud y recopilar la informacion 
* Mejora de creacion de mapa con Folium para visulizacion de prediccion
* Mejora de formato de mapa con Folium

## Soporte 
Actualmente el proyecto se encuentra en desarrollo. Cualquier duda o sugerencia al correo especficiado de los autores