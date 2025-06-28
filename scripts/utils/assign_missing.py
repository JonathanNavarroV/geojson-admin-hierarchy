from InquirerPy import inquirer
from .encoding import fix_encoding


def assign_missing_provinces(adm2, adm1):
    """
    Permite asignar manualmente una región a cada provincia sin región detectada.
    """
    regions = [{"name": fix_encoding(row['shapeName']), "value": idx}
               for idx, row in adm1.iterrows()]

    for idx, row in adm2[adm2['region_index'].isnull()].iterrows():
        print(
            f"\nProvince sin región asignada: {fix_encoding(row['shapeName'])}")
        selected = inquirer.select(
            message="Selecciona region correspondiente: ",
            choices=regions,
            default=None,
        ).execute()

        adm2.at[idx, 'region_index'] = selected


def assign_missing_districts(adm3, adm2):
    """
    Permite asignar manualmente una provincia a cada comuna sin provincia detectada.
    """
    provinces = [{"name": fix_encoding(
        row['shapeName']), "value": idx} for idx, row in adm2.iterrows()]

    for idx, row in adm3[adm3['province_index'].isnull()].iterrows():
        print(
            f"\nDistrict sin province asignada: {fix_encoding(row['shapeName'])}")
        selected = inquirer.select(
            message="Selecciona la province correspondiente: ",
            choices=provinces,
            default=None,
        ).execute()

        adm3.at[idx, 'province_index'] = selected
