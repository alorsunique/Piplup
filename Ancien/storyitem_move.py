# This script should make a copy of the story items in the resources folder

import ast
import os
import shutil
from pathlib import Path

import pandas as pd

from Modules import utility_pack as up

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"
resources_dir = upper_dir / "PycharmProjects Resources" / "Piplup Resources"
storyitem_file = resources_dir / "StoryItem.xlsx"
to_move_storyitem_dir = resources_dir / "To Move StoryItem"

if not to_move_storyitem_dir.exists():
    os.mkdir(to_move_storyitem_dir)

import_dataframe = pd.read_excel(storyitem_file)
account_dict, account_list = up.account_dictionary(otter_dir)

for index, row in import_dataframe.iterrows():
    account = row.iloc[0]
    storyitem_list = ast.literal_eval(row.iloc[1])

    new_account_dir = to_move_storyitem_dir / account

    if not new_account_dir.exists():
        os.mkdir(new_account_dir)

    time_list = []
    for entry in storyitem_list:
        file_split = entry.split(".")
        time_list.append(file_split[0])

    account_dir = account_dict[account] / account
    for file in account_dir.iterdir():
        # print(file.name)
        for entry in time_list:
            if entry in file.name:
                print(f"{entry} | {file.name}")
                new_file_dir = new_account_dir / file.name
                shutil.copy2(file, new_file_dir)
