from scripts.utils.encoding import fix_encoding


def build_structure(adm1, adm2, adm3):
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
    return {
        "country": {
            "name": "Chile",
            "regions": region_list
        }
    }
