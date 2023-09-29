# Package containing most of the functionality

import os
import sys
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from instaloader import Profile
from instaloader import load_structure_from_file

from Modules import download_pack as dp


# Creates a dictionary of all available profiles in the directory
def account_dictionary(directory):
    account_dict = dict()
    account_list = []

    for division in directory.iterdir():
        for account in division.iterdir():
            account_dict[account.name] = division
            account_list.append(account.name)

    return account_dict, account_list


# This should check for the downloaded post
# Create a list for comparison
def offline_post_check(account, account_dict, L_instance):
    L = L_instance
    division_dir = account_dict.get(account)
    account_dir = division_dir / account

    offline_list = []

    for file in account_dir.iterdir():
        if ".json.xz" in file.name:
            structure = load_structure_from_file(L.context, str(file))

            if "Post" in str(structure):
                offline_list.append(structure)

    return offline_list


def update_folder(L_instance, account):
    print(f"Working directory: {Path.cwd()}")

    folder_dir = Path.cwd() / account
    id_dir = folder_dir / "id"

    with open(id_dir, "r") as id_file:
        id_number = id_file.readline()

    username = Profile.from_id(L_instance.context, id_number).username

    print(f"Current username: {username}")

    if username == account:
        print(f"Username retained")
    else:
        print(f"Username mismatch. Renaming {account} to {username}")
        folder_dir.rename(username)
        account = username

    return account


def profile_target(account_dict, otter_dir, net_counter, L_instance, L_checker):
    account = input("Target: ")

    condition_new_account = True  # Assumes target is a new account

    if account in account_dict:
        os.chdir(account_dict.get(account))
        condition_new_account = False  # False indicates a folder is already in the drive
    else:

        # In here, the proper division is selected for the new account
        division_list = []
        for division in otter_dir.iterdir():
            division_list.append(division.name)
        print(f"Available division")
        count = 0
        for entry in division_list:
            print(f"{count}: {entry}")
            count += 1

        while True:
            division_choice = input(f"Select: ")
            try:
                download_division = division_list[int(division_choice)]
                break
            except:
                print(f"Did not catch that")

        division_dir = otter_dir / download_division
        os.chdir(division_dir)

    # Gets the total post to be downloaded
    while True:
        try:
            dl_max = int(input("Total posts to be downloaded: "))
            break
        except:
            print(f"Did not catch that")

    # Gets the download type
    while True:
        try:
            if not condition_new_account:
                dl_type = int(input("1. Run Through | 2. Update | Input: "))
            else:  # If not a new account, download will default to run through
                dl_type = 1
            if dl_type >= 1 and dl_type <= 2:
                break
        except:
            print(f"Did not catch that")

    if dl_type == 1:
        if not condition_new_account:
            offline_list = offline_post_check(account, account_dict, L_checker)
            account = update_folder(L_instance, account)
            while True:
                try:
                    # How many posts to be skipped before compare download becomes regular download
                    max_pass = int(input(f"Pass Amount: "))
                    break
                except:
                    print(f"Did not catch that")
        else:  # Account is new
            max_pass = -1  # Minimum integer value to make the code run
            offline_list = []  # Still need to pass a list but is empty because of new account

        counter, new_dl_count, wait_time = dp.post_compare_download(L_instance, account, offline_list, dl_max,
                                                                    net_counter, max_pass)
    elif dl_type == 2:
        offline_list = offline_post_check(account, account_dict, L_checker)
        # How many posts to be skipped before the update terminates if the next post is already downloaded
        # Basically the lead update code if pass amount is set to 3
        max_dl_skip = int(input(f"Pass Amount: "))
        account = update_folder(L_instance, account)
        counter, new_dl_count, wait_time = dp.post_compare_update(L_instance, account, offline_list, dl_max,
                                                                  net_counter, max_dl_skip)

    sys.stdout.write(f"\r\n")
    print("Account Done")
    print(f"Post Downloaded: {new_dl_count}")
    print(f"Total Wait Time: {wait_time} Seconds")


# Profile sweep will be updated to be a division sweep in the next update of this code
def profile_sweep(resources_dir, otter_dir, account_dict, account_list, net_counter, L_instance, L_checker):
    sweep_box = tk.Tk()
    sweep_box.wm_attributes("-topmost", 1)
    sweep_box.withdraw()

    division_list = []

    for division in otter_dir.iterdir():
        division_list.append(f"{division.name}.txt")

    # Create missing text file if needed

    sweep_dir = resources_dir / "Sweep"
    if not sweep_dir.exists():
        os.mkdir(sweep_dir)

    for entry in division_list:
        text_path = sweep_dir / entry
        if not text_path.exists():
            with open(text_path, "w") as writer:
                writer.close()

    last_entry_list = []

    for text in sweep_dir.iterdir():
        with open(text, 'r') as reader:
            last_entry_list.append(reader.read())
            reader.close()

    while True:
        try:
            print(f"Division List")
            for entry in division_list:
                division_index = division_list.index(entry)
                print(f"{division_index + 1} | {entry.removesuffix('.txt')} | {last_entry_list[division_index]}")
            choice = int(input("Select: "))

            if choice >= 1 and choice <= len(division_list):
                break
        except:
            print(f"Did not catch that")

    work_division = otter_dir / division_list[choice - 1].removesuffix('.txt')
    account_list = []
    for account in work_division.iterdir():
        account_list.append(account.stem)

    if not last_entry_list[choice - 1] == '':
        workable_list = account_list[account_list.index(last_entry_list[choice - 1]) + 1:].copy()
    else:
        workable_list = account_list.copy()

    workable_length = len(workable_list)
    progress_count = 0
    print(f"Length of workable list: {workable_length}")

    for entry in workable_list:

        progress_count += 1

        print(f"Account: {entry}")
        print(f"Current Progress: {progress_count}/{workable_length}")

        while True:
            try:
                dl_max = int(input("Total posts to be downloaded: "))
                max_pass = int(input(f"Pass Amount: "))
                break
            except:
                print(f"Did not catch that")

        account = entry
        os.chdir(account_dict.get(account))

        offline_list = offline_post_check(account, account_dict, L_checker)
        account = update_folder(L_instance, account)
        counter, new_dl_count, wait_time = dp.post_compare_update(L_instance, account, offline_list, dl_max,
                                                                  net_counter, max_pass)

        sys.stdout.write(f"\r\n")
        print("Account Done")
        print(f"Post Downloaded: {new_dl_count}")
        print(f"Total Wait Time: {wait_time} Seconds")

        messagebox.showinfo(f"Sweep", f"{account} Done", parent=sweep_box)

        text_path = sweep_dir / division_list[choice - 1]

        if text_path.exists():
            os.remove(text_path)

        is_last = workable_list[-1] == entry

        if not is_last:
            with open(text_path, 'w') as writer:
                writer.write(account)
                writer.close()

        sleep_second = 30

        print(f"Waiting for {sleep_second} seconds")
        time.sleep(sleep_second)

        while True:
            continueCondition = input(f"Continue Y/N: ").lower()
            if continueCondition == "y":
                break
            elif continueCondition == "n":
                break
            else:
                print(f"Did not catch that")

        if continueCondition == "n":
            break

    sweep_box.destroy()


# Will return the size of the folder of an account
def print_size(size):
    print_size = float(size)

    partition_count = 0

    while print_size >= 1000:
        print_size /= 1000
        partition_count += 1

    if partition_count == 0:
        partition_text = "B"
    elif partition_count == 1:
        partition_text = "KB"
    elif partition_count == 2:
        partition_text = "MB"
    elif partition_count == 3:
        partition_text = "GB"

    print_size_string = f"{round(print_size, 2)} {partition_text}"

    return print_size_string
