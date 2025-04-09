"""This module is made for manage user settings as config files. 
"""

# modules
import json
import sys
from pathlib import Path

# project code
from code.consts import Settings, ConfigKeys, DefaultValue

# packages
from rich import print


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


def write_default_settings(overwrite:bool=False)->bool:
    """Saves the default values in config file."""
    
    default_data = dict()

    default_data[ConfigKeys.DST_EXT.value] = DefaultValue.DST_EXT.value
    default_data[ConfigKeys.SRC_EXT.value] = DefaultValue.SRC_EXT.value
    default_data[ConfigKeys.DST_FOLDER.value] = DefaultValue.DST_FOLDER.value
    default_data[ConfigKeys.SRC_FOLDER.value] = DefaultValue.SRC_FOLDER.value
    default_data[ConfigKeys.QUALITY.value] = DefaultValue.QUALITY.value
    default_data[ConfigKeys.KEEP_TREE.value] = DefaultValue.KEEP_TREE.value
    default_data[ConfigKeys.RECURSIVE.value] = DefaultValue.RECURSIVE.value
    # not implemented yet
    default_data[ConfigKeys.OVERRIDE.value] = DefaultValue.OVERRIDE.value
    default_data[ConfigKeys.THEME.value] = DefaultValue.THEME.value
    default_data[ConfigKeys.LANGUAGE.value] = DefaultValue.LANGUAGE.value
    
    # JSON path
    settings_path = find_json()
    # if config folder doesn't exists it will be created 
    parent_folder = settings_path.parent
    if not parent_folder.is_dir():
        Path.mkdir(parent_folder, parents=True, exist_ok=True)
        print("Settings folder created")

    # if config file doesn't exists it will be created 
    if not settings_path.is_file() or overwrite:
        r = writing_json(settings_path, default_data)
        if r:
            print("Settings file created/overwrote")
        else:
            print("Cannot create settings file")
        return r
    else:
        print("Settings file already exists")
        return False





