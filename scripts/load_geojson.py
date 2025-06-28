import geopandas as gpd


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

# Ejemplo
print("Ejemplo de regiones (ADM1):")
print(adm1[['shapeName']].head())

print("\nEjemplo de provincias (ADM2):")
print(adm2[['shapeName']].head())

print("\nEjemplo de comunas (ADM3):")
print(adm3[['shapeName']].head())
