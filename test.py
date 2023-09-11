import os

directory = "D:\\Projects\\PycharmProjects\\Otter\\Critique Secondaire"

for content in os.listdir(directory):
    print(content)

ini_dir = os.path.join(directory, "desktop.ini")

if os.path.exists(ini_dir):
    os.remove(ini_dir)
    print("Removed")