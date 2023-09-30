# This script should create the CSV file that will keep track of the profiles in the Otter directory
import os
from pathlib import Path

import pandas as pd

from Modules import utility_pack as up

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Test Otter"
resources_dir = upper_dir / "PycharmProjects Resources" / "Piplup Resources"

excel_file = resources_dir / "Test Catalog.xlsx"


def otter_scan(otter_dir, include_status=True):
    otter_list = []
    account_dict, account_list = up.account_dictionary(otter_dir)
    if include_status:
        for entry in account_dict:
            # print(f"Entry: {entry} | Division: {account_dict[entry].name}")
            account_pack = (entry, account_dict[entry].name, 0)
            otter_list.append(account_pack)
    else:
        for entry in account_dict:
            # print(f"Entry: {entry} | Division: {account_dict[entry].name}")
            account_pack = (entry, account_dict[entry].name)
            otter_list.append(account_pack)
    return otter_list


if excel_file.exists():
    # Excel content is read here
    import_dataframe = pd.read_excel(excel_file)
    import_list = import_dataframe.values.tolist()

    # Reference list is created to compare entries from otter directory and entries from the excel file
    reference_import_list = []
    for entry in import_list:
        reference_import_list.append(tuple(entry[:-1]))

    # Converting to set
    otter_set = set(otter_scan(otter_dir, False))
    import_set = set(reference_import_list)

    difference = import_set.difference(otter_set)
    difference_list = []
    print("Import difference")
    for entry in difference:
        print(f"Difference: {entry[0]}")
        difference_list.append(entry[0])

    modified_list = []
    for entry in import_list:
        if entry[0] not in difference_list:
            modified_list.append(entry)

    reference_import_list = []
    for entry in modified_list:
        reference_import_list.append(tuple(entry[:-1]))

    difference = otter_set.difference(import_set)

    print("Otter difference")
    for entry in difference:
        print(f"Difference: {entry[0]}")
        modified_list.append([entry[0], entry[1], 0])

    unique_division = []
    for entry in modified_list:
        if entry[1] not in unique_division:
            unique_division.append(entry[1])

    unique_division = sorted(unique_division)
    updated_list = []

    for division in unique_division:
        division_list = []
        for entry in modified_list:
            if entry[1] == division:
                division_list.append(entry)
        division_list.sort(key=lambda x: x[0])
        updated_list.extend(division_list)

    dataframe = pd.DataFrame(updated_list, columns=['Account', 'Division', 'Create Status'])
    print(dataframe)

    os.remove(excel_file)
    dataframe.to_excel(excel_file, sheet_name='Catalog', index=False)

else:  # Creation of new catalog excel file
    otter_list = otter_scan(otter_dir)
    dataframe = pd.DataFrame(otter_list, columns=['Account', 'Division', 'Create Status'])
    dataframe.to_excel(excel_file, sheet_name='Catalog', index=False)
