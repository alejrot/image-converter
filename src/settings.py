"""This module is made for manage user settings as config files. 
"""

# modules
import json
import sys
from pathlib import Path
from copy import deepcopy

# project code
from .consts import Settings, ConfigKeys, DefaultValue

# packages
from rich import print as print


default_data = {
    f"{ConfigKeys.DST_EXT.value}" : DefaultValue.DST_EXT.value,
    f"{ConfigKeys.SRC_EXT.value}" : DefaultValue.SRC_EXT.value,
    f"{ConfigKeys.DST_FOLDER.value}" : DefaultValue.DST_FOLDER.value,
    f"{ConfigKeys.SRC_FOLDER.value}" : DefaultValue.SRC_FOLDER.value,
    f"{ConfigKeys.QUALITY.value}" : DefaultValue.QUALITY.value,
    f"{ConfigKeys.KEEP_TREE.value}" : DefaultValue.KEEP_TREE.value,
    f"{ConfigKeys.RECURSIVE.value}" : DefaultValue.RECURSIVE.value,
    f"{ConfigKeys.OVERRIDE.value}" : DefaultValue.OVERRIDE.value,
    f"{ConfigKeys.THEME.value}" : DefaultValue.THEME.value,
    f"{ConfigKeys.LANGUAGE.value}" : DefaultValue.LANGUAGE.value,
}


def reading_json(settings_path)-> dict|None:
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


def writing_json(settings_path, dict_data)->bool:
    """Writes settings data as JSON file.
    Returns 'True if file is created, otherwise returns 'False'.
    """
    with open(settings_path, 'w', encoding='utf-8') as json_file:
        json.dump(dict_data, json_file, indent=4)

    return Path(settings_path).is_file()



def find_json()->str:
    """Returns the data path to the JSON settings file."""

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
    settings_path = settings_path.joinpath(Settings.FILENAME.value)
    settings_path = settings_path.expanduser()

    return settings_path


def write_default_settings()->bool:
    """Saves the default values in config file."""
    
    # JSON path
    settings_path = find_json()
    # if config folder doesn't exists it will be created 
    parent_folder = settings_path.parent
    if not parent_folder.is_dir():
        Path.mkdir(parent_folder, parents=True, exist_ok=True)
        print("Settings folder created")

    # if config file doesn't exists it will be created 
    if writing_json(settings_path, default_data):
        print("Settings file created/overwrote")
        return True
    else:
        print("Cannot create settings file")
        return False 



def read_default_settings()->dict:
    """Reads the default values from config file. If it doesn't exist then default data is returned.
    """
    # JSON path
    settings_path = find_json()
    # if config file doesn't exists it returns a copy of default data
    data = reading_json(settings_path)
    
    if data is None:
        print("No settings file found.")
        return deepcopy(default_data)
    else:
        print("Settings file read.")

        # missing data added with default values
        default_keys = default_data.keys()
        data_keys = data.keys()
        full_data = deepcopy(data)
        for key in default_keys:
            if key not in data_keys: 
                full_data[key] = default_data[key]

        return full_data

