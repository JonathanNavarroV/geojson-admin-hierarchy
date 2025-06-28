import geopandas as gpd
import os
import json
from utils.encoding import fix_encoding
from utils.geo_operations import find_parent
from utils.builder import build_structure
from utils.assign_missing import assign_missing_adm2, assign_missing_adm3
from utils.file_selector import select_country_data_folder, detect_adm_files

# Seleccionar la carpeta del país con la consola interactiva
data_folder = select_country_data_folder()

# Se detectan automáticamente los archivos ADM1, ADM2 y ADM3
adm_paths = detect_adm_files(data_folder)
ADM1_PATH = adm_paths["adm1"]
ADM2_PATH = adm_paths["adm2"]
ADM3_PATH = adm_paths["adm3"]

# Cargar archivos GeoJSON como GeoDataFrames
adm1 = gpd.read_file(ADM1_PATH)
adm2 = gpd.read_file(ADM2_PATH)
adm3 = gpd.read_file(ADM3_PATH) if ADM3_PATH else None  # Opcional

# Convertir a CRS métrico (EPSG:3857) para el cálculo espacial
adm1 = adm1.to_crs(epsg=3857)
adm2 = adm2.to_crs(epsg=3857)
if adm3 is not None:
    adm3 = adm3.to_crs(epsg=3857)

# Calcular centroides para detectar las relaciones jerárquicas
adm1['centroid'] = adm1.geometry.centroid
adm2['centroid'] = adm2.geometry.centroid
if adm3 is not None:
    adm3['centroid'] = adm3.geometry.centroid

# Asignar relaciones
adm2['adm1_index'] = find_parent(adm2, adm1)
if adm3 is not None:
    adm3['adm2_index'] = find_parent(adm3, adm2)

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

# Construir estructura anidada (ADM1 -> ADM2 -> ADM3)
country_structure = build_structure(adm1, adm2, adm3)

# Guardar archivo utilizando el nombre de la carpeta seleccionada
country_name = os.path.basename(data_folder)
output_filename = f"{country_name}_administrative_structure_nested.json"
output_path = os.path.join("output", output_filename)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(country_structure, f, ensure_ascii=False, indent=2)

print("✅ Archivo generado con éxito:", output_path)
