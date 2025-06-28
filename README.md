# Procesador de límites administrativos 🌍🗺️

Script en Python para procesar archivos GeoJSON de divisiones administrativas (regiones, provincias, comunas o equivalentes) de cualquier país, generando una estructura JSON jerárquica y corregida para uso en análisis o aplicaciones GIS.

---

## 👨‍💻 Tecnologías

- Python 3
- GeoPandas
- Shapely
- JSON
- Proyección y cálculo espacial (CRS EPSG:4326 / EPSG:3857)

---

## ✅ Funcionalidades implementadas

- Carga de múltiples archivos GeoJSON de niveles administrativos.
- Cálculo de centroides para relacionar jerarquías territoriales (padres-hijos).
- Corrección automática de encoding para nombres con caracteres especiales.
- Generación de un JSON anidado con la estructura país → regiones → provincias → comunas.
- Identificación y reporte de posibles datos sin asignar (comunas sin provincia, provincias sin región).

---

## Instalación y uso

### 1. Clona el repositorio

```bash
git clone https://github.com/TU_USUARIO/admin-boundaries-processor.git
cd admin-boundaries-processor
```

### 2. Instala las dependencias

```bash
pip install geopandas shapely
```

### 3. Coloca tus archivos GeoJSON

Agrega los archivos GeoJSON simplificados con los niveles administrativos (ej. `geoBoundaries-COUNTRY-ADM1_simplified.geojson`, `geoBoundaries-COUNTRY-ADM2_simplified.geojson`, `geoBoundaries-COUNTRY-ADM3_simplified.geojson`) en la carpeta raíz.

### 4. Ejecuta el script

```bash
python adm_cleaner.py
```

### 5. Obtén el JSON resultante

El archivo `country_administrative_structure_nested.json` se generará con la estructura jerárquica para uso directo.

---

## 📂 Fuentes de datos
Los archivos GeoJSON de divisiones administrativas utilizados en este proyecto se descargaron de [GeoBoundaries](https://www.geoboundaries.org/), una plataforma abierta que provee datos geoespaciales de límites administrativos a nivel mundial.

---

## 📌 Estado actual

Funcional y probado con datos administrativos de Chile. Adaptable para otros países con archivos GeoJSON similares.

---

## ✨ Autor

[Jonathan Navarro](https://github.com/JonathanNavarroV)
