import geopandas as gpd
import os
import json
from utils.encoding import fix_encoding
from utils.geo_operations import find_parent
from utils.builder import build_structure
from utils.assign_missing import assign_missing_provinces, assign_missing_districts

# Rutas
ADM1_PATH = "data/chile/geoBoundaries-CHL-ADM1_simplified.geojson"
ADM2_PATH = "data/chile/geoBoundaries-CHL-ADM2_simplified.geojson"
ADM3_PATH = "data/chile/geoBoundaries-CHL-ADM3_simplified.geojson"

# Cargar archivos
adm1 = gpd.read_file(ADM1_PATH)
adm2 = gpd.read_file(ADM2_PATH)
adm3 = gpd.read_file(ADM3_PATH)

# Se convierte a CRS proyectado (EPSG:3857) para calcular correctamente los centroides en metros
adm1 = adm1.to_crs(epsg=3857)
adm2 = adm2.to_crs(epsg=3857)
adm3 = adm3.to_crs(epsg=3857)

# Se calcular el centroide de cada geometría
adm1['centroid'] = adm1.geometry.centroid
adm2['centroid'] = adm2.geometry.centroid
adm3['centroid'] = adm3.geometry.centroid

# Se asignan las relaciones
adm3['province_index'] = find_parent(adm3, adm2)
adm2['region_index'] = find_parent(adm2, adm1)

# Provincias sin región asignada
missing_regions = adm2[adm2['region_index'].isnull()]
print(f"Provincias sin región: {len(missing_regions)}")
for idx, row in missing_regions.iterrows():
    print(f"  - ID: {idx}, Nombre: {fix_encoding(row.get('shapeName', ''))}")

# Comunas sin provincia asignada
missing_provinces = adm3[adm3['province_index'].isnull()]
print(f"Comunidades sin provincia: {len(missing_provinces)}")
for idx, row in missing_provinces.iterrows():
    print(f"  - ID: {idx}, Nombre: {fix_encoding(row.get('shapeName', ''))}")

if not missing_regions.empty:
    assign_missing_provinces(adm2, adm1)

if not missing_provinces.empty:
    assign_missing_districts(adm3, adm2, adm1)

# Se construye la estructura
country_structure = build_structure(adm1, adm2, adm3)

# Guardar archivo
output_path = os.path.join(
    "output", "country_administrative_structure_nested.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(country_structure, f, ensure_ascii=False, indent=2)

print("✅ Archivo generado con éxito:", output_path)
