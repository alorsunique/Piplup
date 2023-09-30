# List the accounts in the Otter directory
# Also shows the size of each account

import os
from pathlib import Path

from Modules import utility_pack as up

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"

account_dict, account_list = up.account_dictionary(otter_dir)

count = 0
total_size = 0

for account in account_list:
    size = 0
    count += 1
    account_dir = Path(account_dict[account]) / account
    xz_count = 0
    for file in account_dir.iterdir():
        file_name = str(file.name)
        if ".xz" in file_name and "UTC" in file_name:
            xz_count += 1

        size += os.path.getsize(file)
        total_size += os.path.getsize(file)

    print_size = up.print_size(size)

    print(f"{count} | {account_dir.parent.name} | {account} | Downloaded: {xz_count} | Size: {print_size}")

print(f"Total Size: {up.print_size(total_size)}")
