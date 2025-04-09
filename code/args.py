"""This module manages the program arguments and reads config values as default.
"""

import argparse

from code.consts import ConfigKeys
from code.settings import reading_json, find_json, write_default_settings

PROGRAM_NAME = "image-converter"


# create default config files if it doesnt exist
write_default_settings()
# read config file
user_dict = reading_json(find_json())


# new arguments parser
parser = argparse.ArgumentParser(
    prog=PROGRAM_NAME,
    # usage='%(prog)s [options]',
    usage=f'{PROGRAM_NAME} [options]',
    description='Converts the input images to the chosen extention.',
    # epilog='Text at the bottom of help',
    )


parser.version = '0.0'

# program version
parser.add_argument(
    '-v',
    '--version',
    action='version',
    )

input_options = parser.add_argument_group()
input_options.title = "Input options"
input_options.description = "Chooses image's source between a folder's path and an image path's list."


# source folder
input_options.add_argument(
    '-sf',
    '--src-folder',
    type=str,
    default = user_dict[ConfigKeys.SRC_FOLDER.value],
    required=False,
    help="Source folder's path. Images will be searched there."
    )

# source image extention
input_options.add_argument(
    '-se',
    '--src-ext',
    type=str,
    default=user_dict[ConfigKeys.SRC_EXT.value],
    # choices=['.jpg', '.png', '.webp', '.jpeg', '.bmp'],
    required=False,
    help="Image's extention to be searched and converted. Values: '.bmp', '.webp', ect."
    )

# recursive search
input_options.add_argument(
    '-r',
    '--recursive',
    action='store_true',
    help="Enables the recursive search in source folder."
    )

# source images
input_options.add_argument(
    '-si',
    '--src-images',
    type=str,
    nargs="+",
    required=False,
    help="Source image's list. Ignores all other input options."
    )

output_options = parser.add_argument_group()
output_options.title = "Output options"
output_options.description = "Changes output properties: output folder, extention, folder tree and quality."


# destiny folder
output_options.add_argument(
    '-df',
    '--dst-folder',
    type=str,
    default=user_dict[ConfigKeys.DST_FOLDER.value],
    required=False,
    help="Destiny folder's path."
    )

# destiny image extention
output_options.add_argument(
    '-de',
    '--dst-ext',
    type=str,
    default=user_dict[ConfigKeys.DST_EXT.value],
    required=False,
    help="Desired image's extention. Values: '.jpg', '.png', ect."
    )


# keep image organization
output_options.add_argument(
    '-k',
    '--keep-tree',
    action='store_true',
    help="Replies the folder's source image organization at output. Only works with recursive searching."
    )


# quality
output_options.add_argument(
    '-q',
    '--quality',
    type=int,
    default=user_dict[ConfigKeys.QUALITY.value],
    required=False,
    help='Quality percent. Higher quality means less losses but hight file size.'
    )


if __name__=="__main__":

    # help reading in program
    # parser.print_help()

    # arguments reading
    args = parser.parse_args()
    print(args)


    # forcing input values
    # print(parser.parse_args(['-kr', '-de', '.png', '-df','.']))