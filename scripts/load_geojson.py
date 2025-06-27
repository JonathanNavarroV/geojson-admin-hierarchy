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


# Rutas
ADM1_PATH = "data/chile/geoBoundaries-CHL-ADM1_simplified.geojson"
ADM2_PATH = "data/chile/geoBoundaries-CHL-ADM2_simplified.geojson"
ADM3_PATH = "data/chile/geoBoundaries-CHL-ADM3_simplified.geojson"

# Cargar archivos
adm1 = gpd.read_file(ADM1_PATH)
adm2 = gpd.read_file(ADM2_PATH)
adm3 = gpd.read_file(ADM3_PATH)

# Ejemplo
print("Ejemplo de regiones (ADM1):")
print(adm1[['shapeName']].head())

print("\nEjemplo de provincias (ADM2):")
print(adm2[['shapeName']].head())

print("\nEjemplo de comunas (ADM3):")
print(adm3[['shapeName']].head())
