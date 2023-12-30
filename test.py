import os
from pathlib import Path

import pandas as pd
from instaloader import Instaloader
from instaloader import load_structure_from_file

from Modules import utility_pack as up

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"
resources_dir = upper_dir / "PycharmProjects Resources" / "Piplup Resources"

account_dict, account_list = up.account_dictionary(otter_dir)
L = Instaloader()

column_list = ["Account", "Story List"]
dataframe = pd.DataFrame(columns=column_list)


def add_row_to_dataframe(df, row_data):
    df = df._append(row_data, ignore_index=True)
    return df


for account in account_list:
    print(f"Current Account: {account}")
    account_dir = account_dict[account] / account

    story_list = []

    for file in account_dir.iterdir():
        if ".xz" in file.name:
            structure = load_structure_from_file(L.context, str(file))
            string_structure = str(structure)
            if "StoryItem" in str(structure):
                story_list.append(file.name)

    if len(story_list) > 0:
        string_story = repr(story_list)
        row = dict()
        row["Account"] = account
        row["Story List"] = string_story

        dataframe = add_row_to_dataframe(dataframe, row)

storyitem_file = resources_dir / "StoryItem.xlsx"

if storyitem_file.exists():
    os.remove(storyitem_file)

dataframe.to_excel(storyitem_file, sheet_name='Catalog', index=False)
