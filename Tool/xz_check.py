# This compares the .xz files in the profiles to post
# Essentially this checks for incomplete deletion

import os

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

        xz_list_copy = xz_list.copy()

        with_image_list = []

        for file in os.listdir(account_dir):
            if ".jpg" in file:

                initial_entry_split = file.split(".")

                entry_split = initial_entry_split[0].split("_")

                clean_string = f"{entry_split[0]}_{entry_split[1]}_{entry_split[2]}"

                if clean_string not in with_image_list:
                    with_image_list.append(clean_string)

        for image in with_image_list:
            for xz in xz_list:
                if image in xz:
                    xz_list_copy.remove(xz)

        print(f"{account} | {xz_list_copy}")
