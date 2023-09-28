# Package containing most of the functionality

import os
import sys
import time
from pathlib import Path

from instaloader import Profile
from instaloader import load_structure_from_file

from Modules import download_pack as dp


# Creates a dictionary of all available profiles in the directory
def account_dictionary(directory):
    account_dict = dict()
    account_list = []

    for division in os.listdir(directory):
        division_dir = os.path.join(directory, division)
        for account in os.listdir(division_dir):
            account_dict[account] = division_dir
            account_list.append(account)

    # account_list = sorted(account_list)

    return account_dict, account_list


# This should check for the downloaded post
# Create a list for comparison
def offline_post_check(account, account_dict, L_instance):
    L = L_instance
    division_dir = account_dict.get(account)
    account_dir = os.path.join(division_dir, account)

    offline_list = []

    for file in os.listdir(account_dir):
        if ".json.xz" in file:
            file_dir = os.path.join(account_dir, file)

            structure = load_structure_from_file(L.context, file_dir)

            if "Post" in str(structure):
                offline_list.append(load_structure_from_file(L.context, file_dir))

    return offline_list


def update_folder(L_instance, account):
    print(f"Working directory: {Path.cwd()}")

    folder_dir = Path.cwd() / account
    id_dir = folder_dir / "id"

    with open(id_dir, "r") as id_file:
        id_number = id_file.readline()

    username = Profile.from_id(L_instance.context, id_number).username

    print(f"Username: {username}")

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

        division_list = os.listdir(otter_dir)
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

        os.chdir(os.path.join(otter_dir, download_division))

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
    print("Post Downloaded: " + str(new_dl_count))
    print("Total Wait Time: " + str(wait_time) + " Seconds")


# Profile sweep will be updated to be a division sweep in the next update of this code
def profile_sweep(project_dir, account_dict, account_list, net_counter, L_instance, L_checker):
    info_text = ["Run Through.txt", "Lead Update.txt", "Compare Update.txt"]

    info_dir = os.path.join(project_dir, "../Information")
    os.chdir(info_dir)

    # Create missing text file if needed

    for entry in info_text:
        if not os.path.exists(os.path.join(info_dir, entry)):
            with open(entry, 'w') as writer:
                writer.close()

    last_entry_list = []

    for entry in info_text:
        with open(entry, 'r') as reader:
            last_entry_list.append(reader.read())
            reader.close()

    print(f"Run Through: {last_entry_list[0]}")
    print(f"Lead Update: {last_entry_list[1]}")
    print(f"Compare Update: {last_entry_list[2]}")

    while True:
        try:

            print(f"Now select which sweep to continue")
            print(f"1: Run Through")
            print(f"2: Lead Update")
            print(f"3: Compare Update")

            choice = int(input("Select: "))

            if choice >= 1 and choice <= 3:
                break

        except:
            print(f"Did not catch that")

    if not last_entry_list[choice - 1] == '':
        workable_list = account_list[account_list.index(last_entry_list[choice - 1]) + 1:].copy()
    else:
        workable_list = account_list.copy()

    workable_length = len(workable_list)
    progress_count = 0
    print(f"Length of workable list: {workable_length}")

    exception_list = []

    for entry in workable_list:

        progress_count += 1

        print("Account: " + entry)
        print("Current Progress: " + str(progress_count) + "/" + str(workable_length))

        while True:
            try:
                dl_max = int(input("Total posts to be downloaded: "))
                break
            except:
                print(f"Did not catch that")

        account = entry
        os.chdir(account_dict.get(account))

        if choice == 1:
            try:
                counter, new_dl_count, wait_time = dp.post_download(L_instance, account, dl_max, net_counter)
            except:
                new_dl_count = 0
                exception_list.append(entry)

        elif choice == 2:
            dl_max = 65536
            try:
                counter, new_dl_count, wait_time = dp.post_lead_update(L_instance, account, dl_max, net_counter)
            except:
                new_dl_count = 0
                exception_list.append(entry)
        elif choice == 3:
            try:
                offline_list = offline_post_check(account, account_dict, L_checker)
                counter, new_dl_count, wait_time = dp.post_compare_update(L_instance, account, offline_list, dl_max,
                                                                          net_counter)
            except:
                new_dl_count = 0
                exception_list.append(entry)

        sys.stdout.write(f"\r\n")
        print("Account Done")
        print("Post Downloaded: " + str(new_dl_count))
        print("Total Wait Time: " + str(wait_time) + " Seconds")

        os.chdir(info_dir)

        if os.path.exists(os.path.join(info_dir, info_text[choice - 1])):
            os.remove(os.path.join(info_dir, info_text[choice - 1]))

        with open(info_text[choice - 1], 'w') as writer:
            writer.write(entry)
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