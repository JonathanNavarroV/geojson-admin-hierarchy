# Procesador de límites administrativos 🌍🗺️

Script en Python para procesar archivos GeoJSON de divisiones administrativas (ADM1, ADM2, ADM3 o equivalentes) de cualquier país, generando una estructura JSON jerárquica y corregida para uso en análisis o aplicaciones GIS.

---

## 👨‍💻 Tecnologías

- Python 3
- [GeoPandas](https://geopandas.org/en/v1.1.1/)
- [Shapely](https://shapely.readthedocs.io/en/2.1.1/)
- JSON
- Proyección y cálculo espacial (CRS EPSG:4326 / EPSG:3857)

---

## ✅ Funcionalidades implementadas

- Carga automática de archivos GeoJSON desde la carpeta data/.
- Soporte para países con 2 o 3 niveles administrativos (ADM3 es opcional).
- Detección automática de archivos geoBoundaries-COUNTRY-ADMx_simplified.geojson.
- Cálculo de centroides para establecer relaciones jerárquicas (padre → hijo).
- Corrección automática de caracteres mal codificados (tildes, eñes, etc.).
- Generación de un JSON anidado con la estructura:

```scss
country → adm1 → adm2 → adm3 (si aplica)
```

- Detección de unidades administrativas huérfanas (ADM2 sin ADM1, ADM3 sin ADM2).
- Asignación manual e interactiva desde la consola para corregir estos casos.

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

Copia los archivos `geoBoundaries-...` en una subcarpeta dentro de `data/`, por ejemplo:

```bash
data/chile/
  ├─ geoBoundaries-CHL-ADM1_simplified.geojson
  ├─ geoBoundaries-CHL-ADM2_simplified.geojson
  ├─ geoBoundaries-CHL-ADM3_simplified.geojson (opcional)
```

> 📁 El nombre de la carpeta será usado como el nombre del país en la estructura JSON final.

### 4. Ejecuta el script

```bash
python .\scripts\load_geojson.py
```

Durante la ejecución, se te pedirá seleccionar interactivamente el país (carpeta en data/) y se detectarán automáticamente los archivos correspondientes a ADM1, ADM2 y ADM3.

- Si existen divisiones administrativas sin jerarquía asignada, se activará una interfaz interactiva en consola para asignarlas manualmente.

### 5. Obtén el JSON resultante

Se generará un archivo JSON jerárquico en la carpeta `output/`, por ejemplo:

```bash
output/chile_administrative_structure_nested.json
```

---

## 📦 Estructura del JSON generado

El script genera un archivo `.json` con una estructura jerárquica basada en los niveles administrativos del país seleccionado.

### Ejemplo (con ADM3):

```json
{
	"country": {
		"name": "chile",
		"adm1": [
			{
				"id": "0",
				"name": "Región Metropolitana",
				"adm2": [
					{
						"id": "12",
						"name": "Provincia de Santiago",
						"adm3": [
							{
								"id": "101",
								"name": "Comuna de Ñuñoa"
							},
							{
								"id": "102",
								"name": "Comuna de Providencia"
							}
						]
					}
				]
			}
		]
	}
}
```

### Ejemplo (sin ADM3):

```json
{
	"country": {
		"name": "argentina",
		"adm1": [
			{
				"id": "0",
				"name": "Buenos Aires",
				"adm2": [
					{
						"id": "15",
						"name": "Partido de La Matanza"
					}
				]
			}
		]
	}
}
```

> 🔁 Los campos id corresponden al índice de cada unidad administrativa en el archivo original.
>
> ✍️ Los nombres son limpiados y corregidos automáticamente para evitar errores de codificación.

---

## 📂 Fuentes de datos

Los archivos GeoJSON de divisiones administrativas utilizados en este proyecto se descargaron de [GeoBoundaries](https://www.geoboundaries.org/), una plataforma abierta que provee datos geoespaciales de límites administrativos a nivel mundial.

---

## 📌 Estado actual

Funcional y probado con datos administrativos de Chile y Argentina. Adaptable para otros países con archivos GeoJSON similares y jerarquías de 2 o 3 niveles.

---

## ✨ Autor

[Jonathan Navarro](https://github.com/JonathanNavarroV)
