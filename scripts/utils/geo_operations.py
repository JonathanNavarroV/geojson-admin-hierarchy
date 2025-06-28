def find_parent(child_gdf, parent_gdf, child_centroid_col='centroid'):
    """
    Para cada geometría en child_gdf, busca el polígono padre en parent_gdf que contiene su centroide.

    Args:
        child_gdf (GeoDataFrame): GeoDataFrame con las geometrías hijas (por ejemplo, ADM3).
        parent_gdf (GeoDataFrame): GeoDataFrame con las geometrías padres (por ejemplo, ADM2).
        child_centroid_col (str): Nombre de la columna con centroides ya calculados en child_gdf.

    Returns:
        List[int or None]: Lista con los índices del padre correspondiente para cada hijo, o None si no hay coincidencia.
    """
    parent_ids = []

    if child_centroid_col not in child_gdf.columns:
        raise ValueError(f"La columna '{child_centroid_col}' no existe en el GeoDataFrame de hijos.")

    for point in child_gdf[child_centroid_col]:
        # Buscar el primer polígono padre que contenga el centroide del hijo
        matched = parent_gdf[parent_gdf.geometry.contains(point)]
        parent_ids.append(matched.index[0] if not matched.empty else None)

    return parent_ids
