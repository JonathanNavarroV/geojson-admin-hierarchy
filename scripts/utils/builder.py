from utils.encoding import fix_encoding


def build_structure(adm1, adm2, adm3):
    """
    Construye la estructura anidada de adm1 -> adm2 -> adm3 desde tres GeoDataFrames.
    Tanto adm2 como adm3 se almacenan como listas para mantener consistencia.

    Args:
        adm1 (GeoDataFrame): Niveles ADM1 (ej. regiones, estados)
        adm2 (GeoDataFrame): Niveles ADM2 (ej. provincias, departamentos)
        adm3 (GeoDataFrame): Niveles ADM3 (ej. comunas, distritos)

    Returns:
        dict: Estructura anidada por país -> adm1 -> adm2 -> adm3
    """

    adm1_list = []

    for idx_adm1, row_adm1 in adm1.iterrows():
        adm1_id = str(int(idx_adm1))
        adm1_name = fix_encoding(row_adm1.get("shapeName", ""))

        # Filtrar adm2 pertenecientes a este adm1
        adm2_in_adm1 = adm2[adm2["adm1_index"] == idx_adm1]

        adm2_list = []
        for idx_adm2, row_adm2 in adm2_in_adm1.iterrows():
            adm2_id = str(int(idx_adm2))
            adm2_name = fix_encoding(row_adm2.get("shapeName", ""))

            # Filtrar adm3 pertenecientes a este adm2
            adm3_in_adm2 = adm3[adm3["adm2_index"] == idx_adm2]

            adm3_list = []
            for idx_adm3, row_adm3 in adm3_in_adm2.iterrows():
                adm3_id = str(int(idx_adm3))
                adm3_name = fix_encoding(row_adm3.get("shapeName", ""))

                adm3_list.append({
                    "id": adm3_id,
                    "name": adm3_name
                })

            adm2_list.append({
                "id": adm2_id,
                "name": adm2_name,
                "adm3": adm3_list
            })

        adm1_list.append({
            "id": adm1_id,
            "name": adm1_name,
            "adm2": adm2_list
        })

    return {
        "country": {
            "name": "Chile",
            "adm1": adm1_list
        }
    }
