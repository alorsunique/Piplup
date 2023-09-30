import os
import json
import shutil
from datetime import datetime

now = datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

project_dir = os.getcwd()

# Change the directory to one level above
split = project_dir.rfind("\\")
new_dir = project_dir[0: split + 1]
os.chdir(new_dir)
working_dir = os.getcwd()

# Takes note of the Otter directory

otter_dir = os.path.join(working_dir, "Otter")

project_folder = []

for division in os.listdir(otter_dir):
    project_folder.append(os.path.join(otter_dir, division))

# Return to project directory
os.chdir(project_dir)

# Takes note of the external directory

external_drive_dir = "E:"
external_sink_dir = os.path.join(external_drive_dir, "External")
from_IG_dir = os.path.join(external_sink_dir, "FromIG")

if not os.path.exists(from_IG_dir):
    os.mkdir(from_IG_dir)

information_dir = os.path.join(project_dir, "Information")
pass_through_dir = os.path.join(information_dir, "Pass Through")

valid_profile_list = []

# Imports the valid profiles

catalog_dir = os.path.join(project_dir, "ToCopyCatalog.txt")

catalogObject = open(catalog_dir, 'r')
catalogAccounts = catalogObject.readlines()

for line in catalogAccounts:
    valid_profile_list.append(line[:-1])

valid_profile_list_length = len(valid_profile_list)
valid_profile_list_count = 0

profile_done_count = 0

profile_done_max = int(input(f"How many profiles will be transferred: "))

for profile in valid_profile_list:

    if profile_done_max == 0:
        break

    valid_profile_list_count += 1
    print(f"Working on {profile} | {valid_profile_list_count}/{valid_profile_list_length}")

    internal_profile_dir = ""

    for division in project_folder:
        potential_dir = os.path.join(division, profile)
        if os.path.exists(potential_dir):
            internal_profile_dir = potential_dir

    external_profile_dir = os.path.join(from_IG_dir, profile)

    present_file_list = []

    if not os.path.exists(external_profile_dir):
        os.mkdir(external_profile_dir)

    for file in os.listdir(external_profile_dir):
        present_file_list.append(file)

    profile_JSON = os.path.join(pass_through_dir, f"{profile}.json")

    json_file = open(profile_JSON, "r")
    data = json.load(json_file)
    to_move_list = data

    transfer_count = 0

    for entry in to_move_list:
        entry_split = entry.split("_")
        compressed_day = entry_split[0].replace("-", "")
        compressed_time = entry_split[1].replace("-", "")

        compressed_string = f"{compressed_day}_{compressed_time}"

        if len(entry_split) == 3:
            compressed_string = compressed_string + ".jpg"
        else:
            entry_split_count = 3

            while entry_split_count < len(entry_split):
                compressed_string += f"_{entry_split[entry_split_count]}"
                entry_split_count += 1

        if compressed_string not in present_file_list:
            source_file = os.path.join(internal_profile_dir, entry)
            sink_file = os.path.join(external_profile_dir, compressed_string)
            shutil.copy2(source_file, sink_file)
            transfer_count += 1

    print(f"Profile: {profile} | Transfer: {transfer_count}")

    profile_done_count += 1
    if profile_done_count >= profile_done_max:
        break



now = datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
print(f"Total Session Run Time: {finish_time - start_time}")
