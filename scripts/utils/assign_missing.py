from InquirerPy import inquirer
from InquirerPy.separator import Separator
from .encoding import fix_encoding


def assign_missing_provinces(adm2, adm1):
    """
    Permite asignar manualmente una región a cada provincia sin región detectada.
    """
    regions = [
        {"name": f"[{idx}] {fix_encoding(row['shapeName'])}", "value": idx}
        for idx, row in adm1.sort_index().iterrows()
    ]

    for idx, row in adm2[adm2['region_index'].isnull()].iterrows():
        print(
            f"\nProvince sin región asignada: {fix_encoding(row['shapeName'])}")
        selected = inquirer.select(
            message="Selecciona region correspondiente: ",
            choices=regions,
            default=None,
        ).execute()

        adm2.at[idx, 'region_index'] = selected


def assign_missing_districts(adm3, adm2, adm1):
    """
    Permite asignar manualmente una provincia a cada comuna sin provincia detectada,
    mostrando las provincias agrupadas por región.
    """
    choices = []
    for idx_reg, row_reg in adm1.sort_index().iterrows():
        region_name = fix_encoding(row_reg['shapeName'])
        choices.append(Separator(f"\n[{idx_reg}] {region_name}"))

        provincias_region = adm2[adm2['region_index'] == idx_reg].sort_index()
        for idx_prov, row_prov in provincias_region.iterrows():
            prov_name = fix_encoding(row_prov['shapeName'])
            choices.append(
                {"name": f"     [{idx_prov}] {prov_name}", "value": idx_prov}
            )

    for idx, row in adm3[adm3['province_index'].isnull()].iterrows():
        print(
            f"\nDistrito sin provincia asignada: {fix_encoding(row['shapeName'])}")
        selected = inquirer.select(
            message="Selecciona la provincia correspondiente:",
            choices=choices,
            default=None,
        ).execute()

        adm3.at[idx, 'province_index'] = selected
