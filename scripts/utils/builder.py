from utils.encoding import fix_encoding


def build_structure(adm1, adm2, adm3):
    """
    Construye la estructura anidada de regions, provinces y districts desde tres GeoDataFrames.
    Tanto provinces como districts se almacenan como listas para mantener consistencia.

    Args:
        adm1 (GeoDataFrame): Niveles ADM1 (Regiones)
        adm2 (GeoDataFrame): Niveles ADM2 (Provincias)
        adm3 (GeoDataFrame): Niveles ADM3 (Comunas o distritos)

    Returns:
        dict: Estructura anidada por pacountry -> regions -> provinces -> districts
    """

    # Se construye diccionario para la anidación
    regions = []

    # Recorrer cada region en el GeoDataFrame de regions (adm1)
    for idx_reg, region in adm1.iterrows():
        # Convertir el índice a string
        region_id = str(int(idx_reg))
        region_name = fix_encoding(region.get('shapeName', ''))

        # Provincias asociadas a esta región
        provinces_in_region = adm2[adm2["region_index"] == idx_reg]

        province_list = []
        for idx_prov, province in provinces_in_region.iterrows():
            province_id = str(int(idx_prov))
            province_name = fix_encoding(province.get("shapeName", ""))

            # Comunas asociadas a esta provincia
            districts_in_province = adm3[adm3["province_index"] == idx_prov]

            district_list = []
            for idx_dist, district in districts_in_province.iterrows():
                district_id = str(int(idx_dist))
                district_name = fix_encoding(district.get("shapeName", ""))

                district_list.append({
                    "id": district_id,
                    "name": district_name
                })

            # Agregar provincia con sus comunas
            province_list.append({
                "id": province_id,
                "name": province_name,
                "districts": district_list
            })

        # Agregar región con sus provincias
        regions.append({
            "id": region_id,
            "name": region_name,
            "provinces": province_list
        })

    # Retornar estructura final
    return {
        "country": {
            "name": "Chile",
            "regions": regions
        }
    }
