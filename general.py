import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox

from instaloader import Instaloader

from Modules import utility_pack as up
from Tool import catalog_create

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"
resources_dir = upper_dir / "PycharmProjects Resources" / "Piplup Resources"
catalog_file = resources_dir / "Catalog.xlsx"
invalid_file = resources_dir / "Invalid.xlsx"

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f"Session Start Time: {current_time}")

L_checker = Instaloader()
L_downloader = Instaloader()

username = "lizyenaliz15"

L_downloader.load_session_from_file(username)  # Here login with credentials

print("Login Done")

net_counter = [0, 0]

task_box = tk.Tk()
task_box.wm_attributes("-topmost", 1)
task_box.withdraw()

while True:
    catalog_create.catalog_create(catalog_file, otter_dir)
    # Get accounts in Otter
    account_dict, account_list = up.account_dictionary(otter_dir)

    print(f"Otter Quantity: {len(account_list)}")

    print(f"0: Exit Loop")
    print(f"1: Download Profile")
    print(f"2: Sweep")

    choice = input(f"Select: ")

    if choice == "0":  # Exit loop
        break
    elif choice == "1":
        up.profile_target(account_dict, otter_dir, net_counter, L_downloader, L_checker, catalog_file, invalid_file)
    elif choice == "2":
        up.profile_sweep(resources_dir, otter_dir, account_dict, net_counter, L_downloader, L_checker, catalog_file, invalid_file)
    else:
        print(f"Did not catch that")

    messagebox.showinfo("Piplup", "Task Done", parent=task_box)

task_box.destroy()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(f"Session End Time: {current_time}")
