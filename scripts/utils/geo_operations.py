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