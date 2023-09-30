# This script should check the downloaded images and find the corrupted ones

import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image

now = datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

# Setting up the directories

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"
resources_dir = upper_dir / "PycharmProjects Resources" / "Piplup Resources"

# Pass through folder

pass_dir = resources_dir / "Pass Through"

if not pass_dir.exists():
    os.mkdir(pass_dir)

# CSV tracker

corrupted_csv = resources_dir / "Corrupted.csv"

if corrupted_csv.exists():
    os.remove(corrupted_csv)

creator = open(corrupted_csv, "x")
creator.close()

corrupted_object = open(corrupted_csv, "w", newline='')
corrupted_writer = csv.writer(corrupted_object, delimiter=",")

directory_list = []
for directory in otter_dir.iterdir():
    directory_list.append(directory)

directory_count = 0
directory_len = len(directory_list)

error_count = 0

global_account_list = []

for directory in directory_list:
    directory_count += 1
    valid_account_list = []

    for account in directory.iterdir():
        valid_account_list.append(account)
        global_account_list.append(account.name)

    valid_count = 0
    valid_account_len = len(valid_account_list)

    for account in valid_account_list:
        valid_count += 1
        clean_pack = []

        profile_JSON_dir = pass_dir / f"{account.name}.json"
        if profile_JSON_dir.exists():
            with open(profile_JSON_dir, "r") as json_file:
                clean_pack = json.load(json_file)

        json_file = open(profile_JSON_dir, "w")

        image_list = []
        for image in account.iterdir():
            if ".jpg" in image.name and image.name not in clean_pack:
                image_list.append(image)

        image_pack = []
        image_count = 0
        image_len = len(image_list)
        for file in image_list:
            image_count += 1
            directory_frac = f"{directory_count}/{directory_len}"
            entry_frac = f"{valid_count}/{valid_account_len}"
            file_frac = f"{image_count}/{image_len}"
            sys.stdout.write(
                f"\r{account.name} | Directory: {directory_frac} | Account: {entry_frac} | File: {file_frac}")

            img_dir = str(file)
            try:
                img = Image.open(img_dir)  # Open the image file

                # Performs the check here. If no error happens, the image is good.
                img_arr = np.array(img)
                img.close()

                clean_pack.append(file.name)

            except (IOError, SyntaxError) as e:
                error_count += 1
                image_pack.append(file.name)

        if len(image_pack) > 0:
            write_pack = [directory, account.name, image_pack]
            corrupted_writer.writerow(write_pack)

        clean_copy_pack = clean_pack.copy()

        for corrupted in image_pack:
            corrupted_split = corrupted.split("_")
            corrupted_string = f"{corrupted_split[0]}_{corrupted_split[1]}"
            print(f"Corrupted String: {corrupted_string}")

            for clean in clean_copy_pack:
                if corrupted_string in clean:
                    print(f"Removing Clean: {clean} | Corresponding Corrupt: {corrupted} | String: {corrupted_string}")
                    clean_pack.remove(clean)

        json.dump(clean_pack, json_file)
        json_file.close()

sys.stdout.write(f"\rComplete. Corrupted Images Found: {error_count}\n")

pass_list = []

for file in pass_dir.iterdir():
    pass_list.append(file.stem)

set_global = set(global_account_list)
set_pass = set(pass_list)
difference_list = list(set_pass.difference(set_global))

for entry in difference_list:
    profile_JSON_dir = pass_dir / f"{entry}.json"

    if profile_JSON_dir.exists():
        print(f"Removing Legacy JSON: {entry}")
        os.remove(str(profile_JSON_dir))

corrupted_object.close()

now = datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
print(f"Total Session Run Time: {finish_time - start_time}")
