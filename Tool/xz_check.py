# This compares the .xz files in the profiles to post
# Essentially this checks for incomplete deletion

import os
import time
from pathlib import Path



project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"
#print(upper_dir)


for division in otter_dir.iterdir():

    for profile in division.iterdir():

        xz_list = []

        for file in profile.iterdir():
            if ".xz" in file.name and "UTC" in file.name:
                xz_list.append(file.stem.replace(".json",""))

        with_image_list = []

        for file in profile.iterdir():

            file_name = file.name
            if ".jpg" in file_name:
                #print(file_name)
                initial_entry_split = file_name.split(".")
                entry_split = initial_entry_split[0].split("_")
                clean_string = f"{entry_split[0]}_{entry_split[1]}_{entry_split[2]}"
                #print(clean_string)
                if clean_string not in with_image_list:
                    with_image_list.append(clean_string)

        xz_list_copy = xz_list.copy()
        for image in with_image_list:
            for xz in xz_list:
                if image in xz:
                    #print(f"Image: {image} | xz: {xz}")
                    xz_list_copy.remove(xz)


        xz_set = set(xz_list)
        with_image_set = set(with_image_list)

        print(profile.name)
        print(xz_list_copy)

        set_list = list(xz_set.difference(with_image_set))
        set_list = sorted(set_list)
        print(set_list)

        print(list(xz_set.difference(with_image_set)).sort())



time.sleep(1000)

project_dir = os.getcwd()

# Change the directory to one level above
split = project_dir.rfind("\\")
new_dir = project_dir[0: split + 1]
os.chdir(new_dir)
working_dir = os.getcwd()

# Takes note of the Otter directory

otter_dir = os.path.join(working_dir, "Otter")

for entry in os.listdir(otter_dir):
    print(entry)

    sub_folder_dir = os.path.join(otter_dir, entry)

    for account in os.listdir(sub_folder_dir):

        account_dir = os.path.join(sub_folder_dir, account)

        xz_list = []

        for file in os.listdir(account_dir):
            if ".xz" in file and "UTC" in file:
                xz_list.append(file)

        # print(xz_list)
        with_image_list = []

        for file in os.listdir(account_dir):
            if ".jpg" in file:

                initial_entry_split = file.split(".")

                entry_split = initial_entry_split[0].split("_")

                clean_string = f"{entry_split[0]}_{entry_split[1]}_{entry_split[2]}"

                if clean_string not in with_image_list:
                    with_image_list.append(clean_string)

        xz_list_copy = xz_list.copy()


        for image in with_image_list:
            for xz in xz_list:
                if image in xz:
                    xz_list_copy.remove(xz)

        print(f"{account} | {xz_list_copy}")
