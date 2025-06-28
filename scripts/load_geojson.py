import geopandas as gpd
import os
import json
from utils.encoding import fix_encoding
from utils.geo_operations import find_parent
from utils.builder import build_structure
from utils.assign_missing import assign_missing_adm2, assign_missing_adm3

# Rutas
ADM1_PATH = "data/argentina/geoBoundaries-ARG-ADM1_simplified.geojson"
ADM2_PATH = "data/argentina/geoBoundaries-ARG-ADM2_simplified.geojson"
ADM3_PATH = ""  # Puede estar vacío si no hay tercer nivel

# Cargar archivos
adm1 = gpd.read_file(ADM1_PATH)
adm2 = gpd.read_file(ADM2_PATH)
adm3 = None
if ADM3_PATH:
    adm3 = gpd.read_file(ADM3_PATH)

# Convertir a CRS para cálculo de centroides
adm1 = adm1.to_crs(epsg=3857)
adm2 = adm2.to_crs(epsg=3857)
if adm3 is not None:
    adm3 = adm3.to_crs(epsg=3857)

# Calcular centroides
adm1['centroid'] = adm1.geometry.centroid
adm2['centroid'] = adm2.geometry.centroid
if adm3 is not None:
    adm3['centroid'] = adm3.geometry.centroid

# Asignar relaciones
if adm3 is not None:
    adm3['adm2_index'] = find_parent(adm3, adm2)
adm2['adm1_index'] = find_parent(adm2, adm1)

# Mostrar elementos sin jerarquía asignada
missing_adm1 = adm2[adm2['adm1_index'].isnull()]
print(f"ADM2 sin ADM1 asignado: {len(missing_adm1)}")
for idx, row in missing_adm1.iterrows():
    print(f"  - ID: {idx}, Nombre: {fix_encoding(row.get('shapeName', ''))}")

if adm3 is not None:
    missing_adm2 = adm3[adm3['adm2_index'].isnull()]
    print(f"ADM3 sin ADM2 asignado: {len(missing_adm2)}")
    for idx, row in missing_adm2.iterrows():
        print(
            f"  - ID: {idx}, Nombre: {fix_encoding(row.get('shapeName', ''))}")

# Asignación manual si es necesario
if not missing_adm1.empty:
    assign_missing_adm2(adm2, adm1)

if adm3 is not None and not missing_adm2.empty:
    assign_missing_adm3(adm3, adm2, adm1)

# Construir estructura
country_structure = build_structure(adm1, adm2, adm3)

# Guardar archivo
output_path = os.path.join(
    "output", "country_administrative_structure_nested.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(country_structure, f, ensure_ascii=False, indent=2)

print("✅ Archivo generado con éxito:", output_path)
