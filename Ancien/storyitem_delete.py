# This script should delete the story items in the Otter profile

import ast
import os
from pathlib import Path

import pandas as pd

from Modules import utility_pack as up

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"
resources_dir = upper_dir / "PycharmProjects Resources" / "Piplup Resources"
storyitem_file = resources_dir / "StoryItem.xlsx"
pass_dir = resources_dir / "Pass Through"

import_dataframe = pd.read_excel(storyitem_file)
account_dict, account_list = up.account_dictionary(otter_dir)

for index, row in import_dataframe.iterrows():
    account = row.iloc[0]
    storyitem_list = ast.literal_eval(row.iloc[1])

    time_list = []
    for entry in storyitem_list:
        file_split = entry.split(".")
        time_list.append(file_split[0])

    account_dir = account_dict[account] / account

    json_file = f"{account}.json"

    json_dir = pass_dir / json_file

    if json_dir.exists():
        os.remove(json_dir)

    for file in account_dir.iterdir():
        # print(file.name)
        for entry in time_list:
            if entry in file.name:
                print(f"{entry} | {file.name}")
                if file.exists():
                    os.remove(file)
