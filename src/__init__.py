# standard libraries
from time import time

# local module
from .args import parser
from .processing import image_threads, processed_counter, processed_event
from .consts import DefaultValue
from .paths import ext_search, relocate_path
from .paths import images_ext
from .settings import reading_json, writing_json, find_json
from .settings import write_default_settings, read_default_settings
from .lang import lang
from .consts import ConfigKeys
from .cli import cli_process


__version__ = '1.5.1'


__all__ = [
    "__version__",
    "parser",
    "image_threads",
    "DefaultValue",
    "ext_search",
    "relocate_path",
    "processed_counter",
    "processed_event", 
    "reading_json",
    "writing_json",
    "find_json",
    "write_default_settings",
    "read_default_settings",
    "lang",
    "ConfigKeys",
    "cli_process",
    "images_ext",
]


def main():
    """Wrapper used """

    parser.version = __version__

    # arguments reading
    input_args = parser.parse_args()

    start = time()
    images_found = cli_process(input_args)
    end = time()

    if images_found is True:
        # print(f"Elapsed time: {(end-start)*1000 :7.6} mseg")
        time_seg = f"{(end-start):5.3}"
        print(f"{lang.t('shell.main.results.time', segs=time_seg)}")

    else:
        print(f"{lang.t('shell.main.results.cancelled')}")

