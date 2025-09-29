# Tropycal_API

##  Intruccion
Tropycal_API es un proyecto desarrollado en python con el objetivo de hacer una API que permita obtener datos de tormentas y huracanes de la NHC, usando como base la libreria Tropycal.

## Librerias y Dependencias

```
pip install "fastapi[standard]" tropycal cartopy shapely folium
```

## How to run 
Dentro del proyecto
```
fastapi dev tro.py
```
[Documentacion FastAPI](https://fastapi.tiangolo.com/#run-it)

## Rutas y llamadas

### "/":
Obtiene y retorna el nombre de las tormentas activas.

### "/data/{storm_name}":
Sustituye ***[storm_name]*** por alguno nombre de tormenta que ya sepas, este regresara su informacion resumida, (id, nombre, fecha de inicio, fecha de finalizacion, viento maximo, presion minima), asi como guarda la informacion completa dentro de una carpeta

### "/images/{storm_name}":
Sustituye ***[storm_name]*** por alguno nombre de tormenta que ya sepas, este regresara la imagen grafica para la visulizacion de la tormenta. asi mismo este guardara la imagen dentro de una carpeta

### "/tormentas/":
La ruta regresa de manera grafica la visualizacion de todas las tormentas actuales


## Licencia

Este proyecto se distribuye bajo la licencia **Creative Commons Atribución 4.0 Internacional (CC BY 4.0)**.

**Autores:**
Pedro Mendoza (ElEmLLi)


Eres libre de usar, modificar y distribuir esta obra, incluso con fines comerciales, siempre y cuando se reconozca la autoría original.

[Licencia CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es)

## Soporte 
Actulamente el proyecto se encuentra en desarrollo. Cualquier duda o sugerencia al correo especficiado de los autores
