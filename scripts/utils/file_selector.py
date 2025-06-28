import os
from InquirerPy import inquirer


def select_country_data_folder(data_dir="data"):
    """
    Muestra un selector interactivo para elegir una subcarpeta dentro de 'data/,
    donde deberían estar los archivos GeoJSON de un país.

    Args:
        data_dir (str): Ruta base donde se almacenan las carpetas de países (por defecto: "data")

    Returns:
        str: Ruta completa a la carpeta seleccionada
    """
    # Listar las subcarpetas dentro de la carpeta data
    folders = [f for f in os.listdir(
        data_dir) if os.path.isdir(os.path.join(data_dir, f))]

    # Si no hay carpetas, se lanza error
    if not folders:
        raise Exception(f"No se encontraron carpetas dentro de '{data_dir}'")

    # Selector interactivo para elegir una carpeta
    selected_folder = inquirer.select(
        message="Selecciona el país/carpeta de datos: ",
        choices=folders
    ).execute()

    # Retorna la ruta completa de la carpeta seleccionada
    return os.path.join(data_dir, selected_folder)


def detect_adm_files(folder_path):
    """
    Detecta los archivos GeoJSON correspondientes a los niveles ADM1, ADM2 y ADM3
    dentro de una carpeta seleccionada. Los nombres de archivo deben contener 'geoBoundaries'
    y 'ADM1', 'ADM2' o 'ADM3'.

    Args:
        folder_path (str): Ruta de la carpeta con archivos GeoJSON

    Returns:
        dict: Diccionario con claves 'adm1', 'adm2' y 'adm3' que contienen las rutas a los archivos correspondientes (o None si ADM3 no se encuentra)

    Raises:
        Exception: Si no se encuentran los archivos ADM1 y ADM2, que son requeridos
    """
    # Listar losr archivos en la carpeta
    files = os.listdir(folder_path)

    # Inicializa con None
    adm_files = {"adm1": None, "adm2": None, "adm3": None}

    # Recorrer todos los archivos y detecta los niveles según su nombre
    for file in files:
        if file.endswith(".geojson") and "geoBoundaries" in file:
            if "ADM1" in file:
                adm_files["adm1"] = os.path.join(folder_path, file)
            elif "ADM2" in file:
                adm_files["adm2"] = os.path.join(folder_path, file)
            elif "ADM3" in file:
                adm_files["adm3"] = os.path.join(folder_path, file)

    # Verificación obligatoria: debe haber al menos ADM1 y ADM2
    if not adm_files["adm1"] or not adm_files["adm2"]:
        raise Exception(
            f"No se encontraron archivos ADM1 y ADM2 válidos en {folder_path}")

    return adm_files
