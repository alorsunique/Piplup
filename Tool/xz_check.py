# This compares the .xz files in the profiles to post
# Essentially this checks for incomplete deletion

from pathlib import Path

project_dir = Path.cwd().parent
upper_dir = project_dir.parent.parent
otter_dir = upper_dir / "Otter"

for division in otter_dir.iterdir():
    for profile in division.iterdir():
        xz_list = []

        # Takes note of the xz files present
        for file in profile.iterdir():
            if ".xz" in file.name and "UTC" in file.name:
                xz_list.append(file.stem.replace(".json", ""))

        # Takes note of the images present
        with_image_list = []
        for file in profile.iterdir():
            file_name = file.name
            if ".jpg" in file_name:
                initial_entry_split = file_name.split(".")
                entry_split = initial_entry_split[0].split("_")
                clean_string = f"{entry_split[0]}_{entry_split[1]}_{entry_split[2]}"
                if clean_string not in with_image_list:
                    with_image_list.append(clean_string)

        # Converts to list for faster manipulation
        # The difference checks for xz files with no images corresponding to them
        xz_set = set(xz_list)
        with_image_set = set(with_image_list)
        difference = xz_set.difference(with_image_set)

        # If differences are found, print the xz files that needs to be deleted
        if len(difference) > 0:
            print(profile.name)
            print(sorted(list(difference)))
