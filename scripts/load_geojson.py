import geopandas as gpd
import os
import json


def fix_encoding(text):
    """
    Corrige errores comunes de codificación cuando los caracteres especiales (como tildes o eñes) se ven mal (ej: 'RegiÃ³n' en lugar de 'Región'). Esto suele ocurrir cuando texto originalmente en UTF-8 fue interpretado como Latin-1.

    Args:
        text (str): Texto posiblemente mal codificado.

    Returns:
        str: Texto corregido si es posible, o el original si no se puede corregir.
    """
    if not text:
        return text
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def find_parent(child_gdf, parent_gdf, child_centroid_col='centroid'):
    """
     Para cada geometría en child_gdf, busca el polígono padre en parent_gdf que contiene su centroide.

     Args:
         child_gdf (GeoDataFrame): GeoDataFrame con las geometrías "hijas" (e.g., comunas).
         parent_gdf (GeoDataFrame): GeoDataFrame con las geometrías "padres" (e.g., provincias).
         child_centroid_col (str): Nombre de la columna con centroides calculados en child_gdf.

     Returns:
         List[int or None]: Lista con los índices del padre correspondiente para cada hijo, o None si no hay coincidencia.
     """
    parent_ids = []
    for point in child_gdf[child_centroid_col]:
        matched = parent_gdf[parent_gdf.geometry.contains(point)]
        if not matched.empty:
            parent_ids.append(matched.index[0])
        else:
            parent_ids.append(None)
    return parent_ids


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

# Se asigna provincia a cada comuna
adm3['province_index'] = find_parent(adm3, adm2)

# Se asigna región a cada provincia
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

# Se construye diccionario para la anidación
regions_dict = {}

# Recorrer cada region en el GeoDataFrame de regions (adm1)
for idx_reg, region in adm1.iterrows():
    # Convertir el índice a string
    region_id = str(int(idx_reg))

    # Se inicializa la region en el diccionadio con su ID, nombre y una lista vacía de provinces
    regions_dict[region_id] = {
        "id": region_id,
        "name": fix_encoding(region.get('shapeName', '')),
        "provinces": {}
    }

# Recorrer cada province en el GeoDataFrame de provinces (adm2)
for idx_prov, province in adm2.iterrows():
    # Se obtiene el índice de la region asociada
    region_idx = province.get('region_index')

    # Si province no tiene region válida, se salta
    if region_idx is None or region_idx not in adm1.index:
        continue

    # Convierte los índices en string
    province_id = str(int(idx_prov))
    region_id = str(int(region_idx))

    # Se agrega la province al diccionario dentro de su region
    regions_dict[region_id]['provinces'][province_id] = {
        "id": province_id,
        "name": fix_encoding(province.get('shapeName', '')),
        "districts": []
    }

# Recorrer cada district en el GeoDataFrame de districts (adm3)
for idx_dist, district in adm3.iterrows():
    # Se obtiene el índice de la province asociada
    province_idx = district.get('province_index')

    # Si district no tiene province válida, se salta
    if province_idx is None or province_idx not in adm2.index:
        continue

    # Convierte el índice de province en string
    province_id = str(int(province_idx))

    # Buscar el índice de la region asociada a esta province
    region_idx = adm2.loc[province_idx].get('region_index')
    if region_idx is None or region_idx not in adm1.index:
        continue

    # Convierte el índice de region en string
    region_id = str(int(region_idx))

    # Se verifica que la region y province estén registradas en el disccionario
    if region_id not in regions_dict:
        continue
    if province_id not in regions_dict[region_id]['provinces']:
        continue

    # Se agrega el district a la lista de districts de su province
    regions_dict[region_id]['provinces'][province_id]['districts'].append({
        "id": str(int(idx_dist)),
        "name": fix_encoding(district.get('shapeName', ''))
    })

# Se convierte el diccionario anidado a lista para el JSON final
region_list = []
for reg_id, reg_data in regions_dict.items():
    province_list = []
    for prov_id, prov_data in reg_data['provinces'].items():
        province_list.append(prov_data)
    reg_data['province'] = province_list
    region_list.append(reg_data)

# Estructura de country
country_structure = {
    "country": {
        "name": "Chile",
        "regions": region_list
    }
}

# Guardar archivo
output_path = os.path.join(
    "output", "country_administrative_structure_nested.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(country_structure, f, ensure_ascii=False, indent=2)

print("✅ Archivo generado con éxito:", output_path)
