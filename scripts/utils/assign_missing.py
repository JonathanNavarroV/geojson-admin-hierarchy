from InquirerPy import inquirer
from InquirerPy.separator import Separator
from .encoding import fix_encoding


def assign_missing_adm2(adm2, adm1):
    """
    Permite asignar manualmente un ADM1 (nivel superior) a cada ADM2 sin asignación detectada.
    """
    adm1_choices = [
        {"name": f"[{idx}] {fix_encoding(row['shapeName'])}", "value": idx}
        for idx, row in adm1.sort_index().iterrows()
    ]

    for idx, row in adm2[adm2['adm1_index'].isnull()].iterrows():
        print(f"\nADM2 sin ADM1 asignado: {fix_encoding(row['shapeName'])}")
        selected = inquirer.select(
            message="Selecciona el ADM1 correspondiente: ",
            choices=adm1_choices,
            default=None,
        ).execute()

        adm2.at[idx, 'adm1_index'] = selected


def assign_missing_adm3(adm3, adm2, adm1):
    """
    Permite asignar manualmente un ADM2 a cada ADM3 sin asignación detectada,
    mostrando los ADM2 agrupados por ADM1.
    """
    choices = []
    for idx_adm1, row_adm1 in adm1.sort_index().iterrows():
        adm1_name = fix_encoding(row_adm1['shapeName'])
        choices.append(Separator(f"\n[{idx_adm1}] {adm1_name}"))

        adm2_in_adm1 = adm2[adm2['adm1_index'] == idx_adm1].sort_index()
        for idx_adm2, row_adm2 in adm2_in_adm1.iterrows():
            adm2_name = fix_encoding(row_adm2['shapeName'])
            choices.append(
                {"name": f"     [{idx_adm2}] {adm2_name}", "value": idx_adm2}
            )

    for idx, row in adm3[adm3['adm2_index'].isnull()].iterrows():
        print(f"\nADM3 sin ADM2 asignado: {fix_encoding(row['shapeName'])}")
        selected = inquirer.select(
            message="Selecciona el ADM2 correspondiente:",
            choices=choices,
            default=None,
        ).execute()

        adm3.at[idx, 'adm2_index'] = selected
