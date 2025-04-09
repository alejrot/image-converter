from enum import Enum
from pathlib import Path






destiny_path = Path("~/converted-images/").expanduser()

# default values for software usage
class Default(Enum):
    """Precharged arguments - used when it's values are not given."""
    QUALITY     = 95
    SRC_FOLDER  = "."
    DST_FOLDER  = str(destiny_path)
    SRC_EXT     = ".webp"
    DST_EXT     = ".jpg"


# keys for user config files: JSON, YAML, ect
class ConfigKeys(Enum):
    """Keys used to read saved configuration values."""
    SRC_FOLDER    = "src_folder"
    DST_FOLDER    = "dst_folder"
    SRC_EXTENTION = "src_extention"
    DST_EXTENTION = "dst_extention"
    OVERRIDE      = "override"
    KEEP_TREE     = "keep_tree"
    RECURSIVE     = "recursive"
    QUALITY       = "quality"
    THEME         = "theme"
    LANGUAGE      = "language"


class Settings(Enum):
    """Settings file and path"""
    FILENAME = "setup.json"
    FOLDER_WINDOWS = "~/image-converter"
    FOLDER_LINUX   = "~/.config/image-converter"
    FOLDER_OTHER   = "~/image-converter"

