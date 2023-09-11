import utility_pack as up
import os


project_dir = os.getcwd()

split = project_dir.rfind("\\")
above_dir = project_dir[0: split + 1]
otter_dir = os.path.join(above_dir, "Otter")

account_dict, account_list = up.account_dictionary(otter_dir)

count = 0

for account in account_list:
    count += 1

    account_dir = os.path.join(account_dict[account],account)

    xz_count = 0

    for file in os.listdir(account_dir):
        if ".xz" in file and "UTC" in file:
            xz_count += 1

    print(f"{count} | {account} | {xz_count}")
