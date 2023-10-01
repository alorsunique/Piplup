import os
import json
import shutil
import time
from datetime import datetime
from pathlib import Path

from Modules import utility_pack as up
import sys
import pandas as pd

now = datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

#project_dir = os.getcwd()
project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"
resources_dir = upper_dir / "PycharmProjects Resources" / "Piplup Resources"

# Change the directory to one level above
#split = project_dir.rfind("\\")
#new_dir = project_dir[0: split + 1]
#os.chdir(new_dir)
#working_dir = os.getcwd()

# Takes note of the Otter directory

#otter_dir = os.path.join(working_dir, "Otter")

#project_folder = []

#for division in os.listdir(otter_dir):
    #project_folder.append(os.path.join(otter_dir, division))

# Return to project directory
#os.chdir(project_dir)

#print(project_folder)

# Takes note of the external directory

external_drive_dir = Path(f"{input('Drive Letter: ').upper()}:")
#print(external_drive_dir)
if not external_drive_dir.exists():
    print("Directory does not exists")

external_dir = external_drive_dir / "External"

if not external_dir.exists():
    os.mkdir(external_dir)

from_IG_dir = external_dir / "FromIG"

if not from_IG_dir.exists():
    os.mkdir(from_IG_dir)

#external_dir = os.path.join(external_drive_dir, "External")
#from_IG_dir = os.path.join(external_dir, "FromIG")


catalog_file = resources_dir / "Catalog.xlsx"
pass_through_dir = resources_dir / "Pass Through"



#information_dir = os.path.join(project_dir, "Information")
#pass_through_dir = os.path.join(information_dir, "Pass Through")

valid_profile_list = []

# Imports the valid profiles

#catalog_dir = os.path.join(project_dir, "ToCopyCatalog.txt")

#catalogObject = open(catalog_dir, 'r')
#catalogAccounts = catalogObject.readlines()


import_dataframe = pd.read_excel(catalog_file)
valid_frame = import_dataframe.loc[import_dataframe["Create Status"]==1]

#print(import_dataframe)
#print(valid_frame)
for index, row in valid_frame.iterrows():
    valid_profile_list.append(row.iloc[0])

#print(valid_profile_list)

account_dict,account_list  = up.account_dictionary(otter_dir)
#print(account_dict)

#for line in catalogAccounts:
    #valid_profile_list.append(line[:-1])

valid_profile_list_length = len(valid_profile_list)
valid_profile_list_count = 0

valid_set = set(valid_profile_list)

transferred_list = []
for entry in from_IG_dir.iterdir():
    print(entry.name)
    transferred_list.append(entry.name)


transfer_set = set(transferred_list)
difference = transfer_set.difference(valid_set)

print(valid_set)
print(transfer_set)

for entry in difference:
    print(f"Diff{entry}")

    print(from_IG_dir / entry)
    shutil.rmtree(from_IG_dir / entry)


profile_done_count = 0

profile_done_max = int(input(f"How many profiles will be transferred: "))

for profile in valid_profile_list:

    if profile_done_max <= 0:
        break

    valid_profile_list_count += 1
    print(f"Working on {profile} | {valid_profile_list_count}/{valid_profile_list_length}")

    #internal_profile_dir = ""

    #for division in project_folder:
        #potential_dir = os.path.join(division, profile)
        #if os.path.exists(potential_dir):
            #internal_profile_dir = potential_dir


    internal_profile_dir = account_dict[profile] / profile

    #print(internal_profile_dir)



    #external_profile_dir = os.path.join(from_IG_dir, profile)

    external_profile_dir = from_IG_dir / profile

    present_file_list = []

    #if not os.path.exists(external_profile_dir):
    if not external_profile_dir.exists():
        os.mkdir(external_profile_dir)

    #for file in os.listdir(external_profile_dir):
    for file in external_profile_dir.iterdir():
        #present_file_list.append(file)
        present_file_list.append(file.name)

    profile_JSON = os.path.join(pass_through_dir, f"{profile}.json")

    #json_file = open(profile_JSON, "r")
    #data = json.load(json_file)
    #to_move_list = data

    with open(profile_JSON, "r") as json_file:
        to_move_list = json.load(json_file)

    #print(to_move_list)

    to_move_list_mod = to_move_list.copy()

    to_move_list = []

    to_move_dict = dict()

    for entry in to_move_list_mod:
        #print(entry)

        file_split =  entry.split(".")

        entry_split = file_split[0].split("_")
        compressed_day = entry_split[0].replace("-", "")
        compressed_time = entry_split[1].replace("-", "")

        compressed_string = f"{compressed_day}_{compressed_time}"

        if len(entry_split) == 3:
            compressed_string = f"{compressed_string}.{file_split[1]}"
        else:
            #print("HEre")
            #entry_split_count = 3

            compressed_string = f"{compressed_string}_{entry_split[3]}.{file_split[1]}"
            #while entry_split_count < len(entry_split):

                #print(f"{entry_split_count}/{len(entry_split)}")

                #compressed_string += f"_{entry_split[entry_split_count]}"
                #entry_split_count += 1

        #print(compressed_string)

        to_move_dict[compressed_string] = entry

        to_move_list.append(compressed_string)

    present_set = set(present_file_list)
    to_move_set = set(to_move_list)

    difference = to_move_set.difference(present_set)
    #print(difference)

    len_difference = len(difference)

    print(f"Total transferables: {len(difference)}")



    transfer_count = 0

    for entry in difference:
        transfer_count += 1
        sys.stdout.write(
            f"\r{transfer_count}/{len_difference}")

        #print(entry)
        #print(to_move_dict[entry])

        source_file = internal_profile_dir / to_move_dict[entry]
        sink_file = external_profile_dir / entry
        shutil.copy2(source_file, sink_file)


    #time.sleep(100000)

    #for entry in to_move_list:
        #entry_split = entry.split("_")
        #compressed_day = entry_split[0].replace("-", "")
        #compressed_time = entry_split[1].replace("-", "")

        #compressed_string = f"{compressed_day}_{compressed_time}"

        #if len(entry_split) == 3:
            #compressed_string = compressed_string + ".jpg"
        #else:
            #entry_split_count = 3

            #while entry_split_count < len(entry_split):
                #compressed_string += f"_{entry_split[entry_split_count]}"
                #entry_split_count += 1

        #if compressed_string not in present_file_list:
            #source_file = os.path.join(internal_profile_dir, entry)
            #sink_file = os.path.join(external_profile_dir, compressed_string)
            #shutil.copy2(source_file, sink_file)
            #transfer_count += 1

    print(f"\nProfile: {profile} | Transfer: {transfer_count}")

    profile_done_count += 1
    if profile_done_count >= profile_done_max:
        break



now = datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
print(f"Total Session Run Time: {finish_time - start_time}")
