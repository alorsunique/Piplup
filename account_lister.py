import utility_pack as up
import os

from pathlib import Path


project_dir = Path.cwd()

current_dir = project_dir
current_dir = current_dir.parent.parent

otter_dir = current_dir / "Otter"

account_dict, account_list = up.account_dictionary(otter_dir)

count = 0

total_size = 0

for account in account_list:

    size = 0

    count += 1

    # account_dir = os.path.join(account_dict[account],account)

    account_dir = Path(account_dict[account]) / account

    xz_count = 0

    # for file in os.listdir(account_dir):
    for file in account_dir.iterdir():
        file_name = str(file.name)
        if ".xz" in file_name and "UTC" in file_name:
            xz_count += 1

        size += os.path.getsize(file)
        total_size += os.path.getsize(file)

    print_size = up.print_size(size)

    print(f"{count} | {account_dir.parent.name} | {account} | Posts Downloaded: {xz_count} | Size: {print_size}")

print(f"Total Size: {up.print_size(total_size)}")