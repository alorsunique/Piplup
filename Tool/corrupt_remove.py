# This should remove all the corrupted images

import ast
import csv
import os
from datetime import datetime

now = datetime.now()
start_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

project_dir = os.getcwd()

info_dir = os.path.join(project_dir, "Information")

source_file = os.path.join(info_dir, "Corrupted.csv")

source_obj = open(source_file, encoding="utf8")
source_reader = csv.reader(source_obj)

rows = []
for row in source_reader:
    rows.append(row)

source_obj.close()

redownload_list = []

for row in rows:

    project_folder = row[0]
    account = row[1]

    redownload_list.append([project_folder, account])

    account_dir = os.path.join(project_folder, account)  # Directory with corrupted image

    remove_list = ast.literal_eval(row[2])
    processed_list = []

    for entry in remove_list:

        initial_entry_split = entry.split(".")

        entry_split = initial_entry_split[0].split("_")

        clean_string = f"{entry_split[0]}_{entry_split[1]}_{entry_split[2]}"
        if clean_string not in processed_list:

            print(f"Process List Append: {clean_string}")

            processed_list.append(clean_string)

    for file in os.listdir(account_dir):

        for reference in processed_list:

            if reference in file:

                remove_file = os.path.join(account_dir, file)

                print(f"File found: {file}")

                if os.path.exists(remove_file):
                    os.remove(remove_file)

redownload_csv = os.path.join(info_dir, "Redownload.csv")

if os.path.exists(redownload_csv):
    os.remove(redownload_csv)

creator = open(redownload_csv, "x")
creator.close()

redownload_object = open(redownload_csv, "w", newline='')
redownload_writer = csv.writer(redownload_object, delimiter=",")

for entry in redownload_list:
    redownload_writer.writerow(entry)

redownload_object.close()

now = datetime.now()
finish_time = now
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
print(f"Total Session Run Time: {finish_time - start_time}")
