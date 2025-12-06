# 🌀 Tropycal_API:

## 🚀 Introducción

**Tropycal_API** es una API desarrollada en Python usando **FastAPI**, diseñada para consultar, procesar y visualizar información en tiempo real de **tormentas tropicales y huracanes** proporcionada por el **National Hurricane Center (NHC)**, utilizando la librería `Tropycal`.

El proyecto genera:

* **Datos en formato JSON**
* **Imágenes PNG**
* **Mapas interactivos HTML**
* **Archivos GIF con trayectoria histórica** (Funcionalidad pendiente)
* **Archivos ZIP** con toda la información de una tormenta
* **Registros automáticos de actividad** en el sistema (`/logs/Tropycal_API.log`)

Todo se almacena en carpetas locales ordenadas por fecha y tormenta dentro del directorio `/data`.

---

## 🛠️ Instalación y Ejecución

### Requisitos

* **Python 3.11** o superior.
* **Conexión a internet** (la librería `Tropycal` descarga los datos del NHC).
* **Git** (para clonar el repositorio).

### Instalación en Windows 🖥️

1.  **Instalar dependencias:**
    Instala las librerías necesarias directamente:

    ```bash
    pip install "fastapi[standard]" tropycal cartopy shapely folium pillow setuptools
    ```

2.  **Clonar el repositorio:**
    Asegúrate de tener Git instalado y usa el siguiente comando (asumiendo que el repositorio es público):

    ```bash
    git clone [URL_DEL_REPOSITORIO]
    cd API-Tropycal
    ```
    *(Nota: Reemplaza `[URL_DEL_REPOSITORIO]` por la URL real de tu proyecto.)*

3.  **Ejecutar el proyecto:**
    Desde la carpeta `/API-Tropycal` ejecuta:

    ```bash
    uvicorn tro:app
    ```

    Opcionalmente, puedes indicar un host o puerto específico:

    ```bash
    uvicorn tro:app --host 0.0.0.0 --port 8080
    ```

---

### Instalación en Linux/macOS 🐧

Se recomienda usar un ambiente virtual para aislar las dependencias del proyecto.

1.  **Crear un ambiente virtual:**

    ```bash
    python3 -m venv venv
    ```

2.  **Activar el ambiente virtual:**

    ```bash
    source venv/bin/activate
    ```

3.  **Clonar el repositorio:**

    ```bash
    git clone [URL_DEL_REPOSITORIO]
    ```
    *(Nota: Reemplaza `[URL_DEL_REPOSITORIO]` por la URL real de tu proyecto.)*

4.  **Entrar a la carpeta del proyecto:**

    ```bash
    cd API-Tropycal
    ```

5.  **Descargar las librerías (dependencias):**

    ```bash
    pip install "fastapi[standard]" tropycal cartopy shapely folium pillow setuptools
    ```

6.  **Ejecutar el programa:**

    ```bash
    uvicorn tro:app
    ```

---

## 🧭 Acceso a la API

Al iniciar, puedes acceder a la API en:

👉 **URL Base:** `http://127.0.0.1:8000`

### Documentación interactiva

* **Swagger UI** → `/docs`
* **Redoc** → `/redoc`

---

## 💾 Estructura de Almacenamiento

Cada solicitud se guarda en carpetas locales con la siguiente estructura:

* Información general de tormentas activas: `/data/AÑO_MES_DIA/Tormentas`
* Información detallada de una tormenta: `/data/AÑO_MES_DIA/NOMBRE_TORMENTA`

Los archivos incluyen **timestamps por rangos horarios de 3 horas** (sistema de *cache* inteligente):

* `00_00.json`, `03_00.json`, ..., `21_00.json` (para datos de tormenta)
* `00_00.png`, `03_00.png`, ..., `21_00.png` (para imágenes de mapas)
* `00_00.html`, `03_00.html`, ..., `21_00.html` (para mapas interactivos)

---

## 🌐 Rutas de la API

### 1. Tormentas Activas y Datos Resumidos

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/data` | Obtiene la **lista de tormentas activas** del NHC. Devuelve los IDs, fecha/hora de captura y zona horaria. Utiliza caché por rango horario para evitar descargas repetidas. |
| `GET` | `/data/{storm_name}` | Obtiene y guarda la **información resumida** de una tormenta activa (ID, nombre, fechas, lat/lon actual, cuenca, viento máx., presión mín.). Guarda la data completa en la carpeta de la tormenta. Si no existe → 404. |

### 2. Mapas e Imágenes de Tormentas Activas

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/images` | Genera (o recupera del caché) una **imagen PNG** con el resumen gráfico de **todas las tormentas activas** (`plot_summary()`). |
| `GET` | `/images/{storm_name}` | Genera (o recupera del caché) una **imagen PNG** de la tormenta seleccionada, incluyendo su **predicción** (`plot_forecast_realtime()`). Si no existe → 404. |
| `GET` | `/dynamic` | Genera (o recupera del caché) un **mapa interactivo HTML** de **todas las tormentas activas**, mostrando trayectoria, intensidad (colores) y predicción futura. |
| `GET` | `/dynamic/{storm_name}` | Genera (o recupera del caché) un **mapa interactivo HTML** enfocado solo en la tormenta especificada (trayectoria, predicción, puntos coloreados, popups de información). Si no existe → 404. |

### 3. Rutas de Datos Históricos por Fecha

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/data_date/{date}` | Recupera una lista de todas las tormentas (`IDs`) que tuvieron registro en la fecha especificada (`AAAA_MM_DD`), combinando todos los rangos horarios. |
| `GET` | `/hour_date/{date}/{storm_name}` | Devuelve una lista de los **rangos horarios** (`00_00`, `03_00`, etc.) para los cuales hay información de la tormenta en la fecha. |
| `GET` | `/data_date/{date}/{storm_name}/{hour}` | Obtiene los **datos resumidos** de una tormenta específica en una fecha y rango horario concretos. Si no existe → 404. |
| `GET` | `/image_date/{date}/{storm_name}/{hour}` | Obtiene la **imagen PNG** de la tormenta específica en una fecha y rango horario concretos. Si no existe → 404. |
| `GET` | `/data_forecast_actual/{storm_name}` | Obtiene los datos de la **predicción** de una tormenta, usando la data más **actual** disponible (basada en el rango horario actual). |
| `GET` | `/data_forecast/{date}/{storm_name}/{hour}` | Obtiene los datos de la **predicción** de una tormenta para una fecha y rango horario específicos. |

### 4. Rutas de Utilidad

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/TraducirJson/{date}/{storm_name}/{hour}` | Lee el JSON de una tormenta en un rango horario y **traduce las claves** del inglés al español, usando un diccionario interno. |
| `GET` | `/zipTormenta/{date}/{storm_name}` | Comprime en un archivo **`.zip`** la carpeta completa de una tormenta para la fecha dada (incluye JSON, PNG, HTML). Devuelve el archivo para su descarga. |
---

## 🆘 Soporte

Este proyecto está en desarrollo activo.

Para dudas o sugerencias, contacta a los autores