# This script should download highlights from an account

import os
import time
from pathlib import Path

from instaloader import Instaloader
from instaloader import Profile
from instaloader import load_structure_from_file

from Modules import utility_pack as up

project_dir = Path.cwd()
upper_dir = project_dir.parent.parent
hailaiteu_dir = upper_dir / "Hailaiteu"
os.chdir(hailaiteu_dir)

L_checker = Instaloader()
L_downloader = Instaloader()

username = "lizyenaliz10"
L_downloader.load_session_from_file(username)  # Here login with credentials

account = input(f"Input account: ")
account_dir = hailaiteu_dir / account

if not account_dir.exists():
    os.mkdir(account_dir)

offline_list = []
for file in os.listdir(account_dir):
    if ".json.xz" in file:
        file_dir = os.path.join(account_dir, file)
        structure = load_structure_from_file(L_checker.context, file_dir)

        if "StoryItem" in str(structure):
            offline_list.append(load_structure_from_file(L_checker.context, file_dir))

id_dir = account_dir / "id"
if id_dir.exists():
    account = up.update_folder(L_downloader, account)

profile = Profile.from_username(L_downloader.context, account)
L_downloader.save_profile_id(profile)  # Download the profile ID
L_downloader.download_profile(profile, profile_pic=True, profile_pic_only=True)  # Download the profile picture

for highlight in L_downloader.get_highlights(profile):
    print(highlight)
    time.sleep(5)
    # highlight is a Highlight object
    for item in highlight.get_items():
        print(item)
        if item not in offline_list:
            L_downloader.download_storyitem(item, '{}'.format(highlight.owner_username))
            time.sleep(5)
        else:
            print("Already downloaded")
