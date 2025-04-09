"""This module is made for manage user settings as config files. 
"""

# modules
import json
import sys
from pathlib import Path

# project code
from code.consts import Settings

# packages
from rich import print


def reading_settings():
    """Reads JSON settings file.
    Returns a dictionary with file data if it is found; otherwise returns 'None'.
    """

    if Path(settings_path).is_file():
        dict_data = dict()
        with open(settings_path, 'r', encoding='utf-8') as json_file:
            dict_data = json.load(json_file)
        return dict_data
    else:
        return None


def writing_settings(dict_data):
    """Writes settings data as JSON file.
    Returns 'True if file is created, otherwise returns 'False'.
    """
    with open(settings_path, 'w', encoding='utf-8') as json_file:
        json.dump(dict_data, json_file, indent=4)

    return Path(settings_path).is_file()




# choosing configuration path
if sys.platform == "linux":

    print("[bold white]System: GNU/Linux")
    settings_path = Path(Settings.FOLDER_LINUX.value)


elif sys.platform == "win32" or sys.platform == "cygwin":

    print("[bold white]System: Windows")
    settings_path = Path(Settings.FOLDER_WINDOWS.value)

else:
    print("[bold white]System: Other systems")
    print("Not implemented")
    settings_path = Path(Settings.FOLDER_OTHER.value)


# composing file path
# settings_path = Path(settings_folder)
settings_path = settings_path.joinpath(Settings.FILENAME.value)
settings_path = settings_path.expanduser()

parent_folder = settings_path.parent

if not parent_folder.is_dir():
    Path.mkdir(parent_folder, parents=True, exist_ok=True)
    print("Folder created")



