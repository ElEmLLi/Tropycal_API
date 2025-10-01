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
fastapi dev tro.py
```
[Documentacion FastAPI](https://fastapi.tiangolo.com/#run-it)

Una vez que el proyecto esté corriendo, podrás acceder a él a través de tu IP de loopback (generalmente el puerto 8000 por defecto): 

*[http://127.0.0.1:8000](http://127.0.0.1:8000)*

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

## Licencia
Este proyecto se distribuye bajo la licencia **Creative Commons Atribución 4.0 Internacional (CC BY 4.0)**.

**Autores:**  
Pedro Mendoza (ElEmLLi)

Eres libre de usar, modificar y distribuir esta obra, incluso con fines comerciales, siempre y cuando se reconozca la autoría original.
[Licencia CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es)

## Funcionalidades a incorporar
* Incorporacion de Logs para el almacenamiento de solicitudes y errores 
* Mejora de creacion de mapa con Folium para visulizacion de prediccion 
* Incorporar hora a la solicitud de data 
* Agregar animacion de trayectoria

## Soporte 
Actulamente el proyecto se encuentra en desarrollo. Cualquier duda o sugerencia al correo especficiado de los autores

