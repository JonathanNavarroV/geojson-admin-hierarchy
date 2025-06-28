# Procesador de límites administrativos 🌍🗺️

Script en Python para procesar archivos GeoJSON de divisiones administrativas (ADM1, ADM2, ADM3 o equivalentes) de cualquier país, generando una estructura JSON jerárquica y corregida para uso en análisis o aplicaciones GIS.

---

## 👨‍💻 Tecnologías

- Python 3
- GeoPandas
- Shapely
- JSON
- Proyección y cálculo espacial (CRS EPSG:4326 / EPSG:3857)

---

## ✅ Funcionalidades implementadas

- Carga de múltiples archivos GeoJSON de niveles administrativos (ADM1, ADM2, ADM3).
- Soporte para países con dos o tres niveles administrativos (ADM3 es opcional).
- Cálculo de centroides para relacionar jerarquías territoriales (padres-hijos).
- Corrección automática de encoding para nombres con caracteres especiales.
- Generación de un JSON anidado con la estructura:
  country → adm1 → adm2 → adm3 (opcional).
- Identificación y reporte de datos sin asignar (por ejemplo, ADM2 sin ADM1, ADM3 sin ADM2).
- Asignación manual interactiva para corregir jerarquías faltantes.

---

## Instalación y uso

### 1. Clona el repositorio

```bash
git clone git@github.com:JonathanNavarroV/geojson-admin-hierarchy.git
cd geojson-admin-hierarchy
```

### 2. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 3. Coloca tus archivos GeoJSON

Agrega los archivos GeoJSON simplificados con los niveles administrativos (ej.
`geoBoundaries-COUNTRY-ADM1_simplified.geojson`,
`geoBoundaries-COUNTRY-ADM2_simplified.geojson`,
`geoBoundaries-COUNTRY-ADM3_simplified.geojson` — este último es opcional)
en la carpeta `data/COUNTRY`.

### 4. Ejecuta el script

```bash
python .\scripts\load_geojson.py
```

Durante la ejecución, si se detectan niveles administrativos sin asignación padre (por ejemplo, ADM2 sin ADM1 o ADM3 sin ADM2), se activará un modo interactivo para asignar manualmente las relaciones faltantes a través de un menú desplegable.

### 5. Obtén el JSON resultante

El archivo `country_administrative_structure_nested.json` se generará en la carpeta `output/` con la estructura jerárquica para uso directo.

---

## 📂 Fuentes de datos

Los archivos GeoJSON de divisiones administrativas utilizados en este proyecto se descargaron de [GeoBoundaries](https://www.geoboundaries.org/), una plataforma abierta que provee datos geoespaciales de límites administrativos a nivel mundial.

---

## 📌 Estado actual

Funcional y probado con datos administrativos de Chile y Argentina. Adaptable para otros países con archivos GeoJSON similares y jerarquías de 2 o 3 niveles.

---

## ✨ Autor

[Jonathan Navarro](https://github.com/JonathanNavarroV)
