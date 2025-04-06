from enum import Enum

from pathlib import Path


destiny_path = Path("~/converted-images/").expanduser()


class Default(Enum):
    QUALITY     = 95
    SRC_FOLDER  = "."
    DST_FOLDER  = str(destiny_path)
    SRC_EXT     = ".webp" 
    DST_EXT     = ".jpg" 
