import os
from datetime import datetime

from instaloader import Instaloader

import utility_pack as up

# Here the Otter directory is determined
# This project and the Otter folder must be in the same directory

project_dir = os.getcwd()

split = project_dir.rfind("\\")
above_dir = project_dir[0: split + 1]
otter_dir = os.path.join(above_dir, "Otter")

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

L_checker = Instaloader()
L_downloader = Instaloader()

username = "lizyenaliz10"

L_downloader.load_session_from_file(username)  # Here login with credentials

print("Login Done")

net_counter = [0, 0]

while True:
    # Get accounts in Otter
    account_dict, account_list = up.account_dictionary(otter_dir)

    print(f"Otter Quantity: {len(account_list)}")

    print(f"0: Exit Loop")
    print(f"1: Download Profile")
    print(f"2: Sweep")
    print(f"3: Re Login")

    choice = input(f"Select: ")

    if choice == "0":  # Exit loop
        break
    elif choice == "1":
        up.profile_target(account_dict, otter_dir, net_counter, L_downloader, L_checker)
    elif choice == "2":
        up.profile_sweep(project_dir, account_dict, account_list, net_counter, L_downloader, L_checker)
    elif choice == "3":
        L_downloader.load_session_from_file(username)
        print(f"Login done")
    else:
        print(f"Did not catch that")

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
