from enum import Enum
# from pathlib import Path






# destiny_path = Path("~/converted-images/").expanduser()

# default values for software usage
class DefaultValue(Enum):
    """Precharged arguments - used when it's values are not given."""
    QUALITY     = 95
    SRC_FOLDER  = "."
    DST_FOLDER  = "~/converted-images/"
    SRC_EXT     = ".webp"
    DST_EXT     = ".jpg"
    KEEP_TREE     = False
    RECURSIVE     = False
    # not implemented yet
    OVERRIDE      = False
    THEME         = "light"
    LANGUAGE      = "EN"

# keys for user config files: JSON, YAML, ect
class ConfigKeys(Enum):
    """Keys used to read saved configuration values."""
    SRC_FOLDER    = "src_folder"
    DST_FOLDER    = "dst_folder"
    SRC_EXT       = "src_extention"
    DST_EXT       = "dst_extention"
    QUALITY       = "quality"
    KEEP_TREE     = "keep_tree"
    RECURSIVE     = "recursive"
    # not implemented yet
    OVERRIDE      = "override"
    THEME         = "theme"
    LANGUAGE      = "language"


class Settings(Enum):
    """Settings file and path"""
    FILENAME = "setup.json"
    FOLDER_WINDOWS = "~/AppData/Local/image-converter"
    FOLDER_LINUX   = "~/.config/image-converter"
    FOLDER_OTHER   = "~/.image-converter"

