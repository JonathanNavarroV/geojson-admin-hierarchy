import geopandas as gpd

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
