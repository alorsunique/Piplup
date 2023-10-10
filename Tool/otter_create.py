# This script should transfer images from valid profiles to an external drive

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from Modules import utility_pack as up

now = datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"
resources_dir = upper_dir / "PycharmProjects Resources" / "Piplup Resources"

output_drive_dir = Path(f"{input('Drive Letter: ').upper()}:")
if not output_drive_dir.exists():
    print("Directory does not exists")
else:
    account_dict, account_list = up.account_dictionary(otter_dir)
    catalog_file = resources_dir / "Catalog.xlsx"
    pass_through_dir = resources_dir / "Pass Through"

    # Create the necessary folders
    external_dir = output_drive_dir / "External"
    if not external_dir.exists():
        os.mkdir(external_dir)
    from_IG_dir = external_dir / "FromIG"
    if not from_IG_dir.exists():
        os.mkdir(from_IG_dir)

    # Importing the valid profiles
    valid_profile_list = []
    import_dataframe = pd.read_excel(catalog_file)
    valid_frame = import_dataframe.loc[import_dataframe["Create Status"] == 1]
    for index, row in valid_frame.iterrows():
        valid_profile_list.append(row.iloc[0])

    valid_profile_list_length = len(valid_profile_list)
    valid_profile_list_count = 0

    # Takes note of the already transferred profiles
    transferred_list = []
    for entry in from_IG_dir.iterdir():
        transferred_list.append(entry.name)

    # Converting to set for better manipulation
    valid_set = set(valid_profile_list)
    transfer_set = set(transferred_list)
    difference = transfer_set.difference(valid_set)

    # Difference set contains the profiles that are present that should not be
    # This part removes the extra profiles
    for entry in difference:
        print(f"Removing: {entry}")
        shutil.rmtree(from_IG_dir / entry)

    profile_done_count = 0
    profile_done_max = int(input(f"How many profiles will be transferred: "))

    total_transfer = 0

    for profile in valid_profile_list:
        if profile_done_max <= 0:
            break

        valid_profile_list_count += 1
        print(f"\nWorking on {profile} | {valid_profile_list_count}/{valid_profile_list_length}")

        # Profile directory in Otter
        internal_profile_dir = account_dict[profile] / profile

        # Profile directory in the output drive
        external_profile_dir = from_IG_dir / profile

        # Creation of profile if not yet present
        if not external_profile_dir.exists():
            os.mkdir(external_profile_dir)

        # Taking note of already transferred files
        present_file_list = []
        for file in external_profile_dir.iterdir():
            present_file_list.append(file.name)

        # Reading the JSON which contains files that can be transferred
        profile_JSON = os.path.join(pass_through_dir, f"{profile}.json")
        with open(profile_JSON, "r") as json_file:
            to_move_list = json.load(json_file)

        # Preprocessing the to move list
        to_move_list_mod = to_move_list.copy()
        to_move_list = []
        to_move_dict = dict()

        for entry in to_move_list_mod:
            file_split = entry.split(".")
            entry_split = file_split[0].split("_")
            compressed_day = entry_split[0].replace("-", "")
            compressed_time = entry_split[1].replace("-", "")
            compressed_string = f"{compressed_day}_{compressed_time}"
            if len(entry_split) == 3:
                compressed_string = f"{compressed_string}.{file_split[1]}"
            else:
                compressed_string = f"{compressed_string}_{entry_split[3]}.{file_split[1]}"

            # Mapping to dictionary
            to_move_dict[compressed_string] = entry
            # Appending the to move list
            to_move_list.append(compressed_string)

        # Converting to set for better manipulation
        present_set = set(present_file_list)
        to_move_set = set(to_move_list)

        # Difference here contains the files that are not in the output already
        difference = to_move_set.difference(present_set)

        len_difference = len(difference)
        print(f"Transferables: {len(difference)}")

        # Transferring happens here
        transfer_count = 0
        for entry in difference:
            transfer_count += 1
            total_transfer += 1
            sys.stdout.write(
                f"\r{transfer_count}/{len_difference}")

            source_file = internal_profile_dir / to_move_dict[entry]
            sink_file = external_profile_dir / entry
            shutil.copy2(source_file, sink_file)

        print(f"\nProfile: {profile} | Transfer: {transfer_count}")
        profile_done_count += 1
        if profile_done_count >= profile_done_max:
            break

print(f"Total files transferred: {total_transfer}")
now = datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
print(f"Total Session Run Time: {finish_time - start_time}")
