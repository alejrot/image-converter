"""This module manages the program arguments and reads config values as default.
"""

import argparse

from .consts import ConfigKeys
from .settings import read_default_settings

from .lang import lang


PROGRAM_NAME = "image-converter"


# read config file
# (if it doesn't exist then default data is returned)
user_dict = read_default_settings()

# new arguments parser
parser = argparse.ArgumentParser(
    prog=PROGRAM_NAME,
    # usage='%(prog)s [options]',
    usage=lang.t('shell.args.usage',PROGRAM_NAME='%(prog)s'),
    description=lang.t('shell.args.description')
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
input_options.title =lang.t('shell.args.input_options.title')
input_options.description =lang.t('shell.args.input_options.description')

# source folder
input_options.add_argument(
    '-sf',
    '--src-folder',
    type=str,
    default = user_dict[ConfigKeys.SRC_FOLDER.value],
    required=False,
    help=lang.t('shell.args.input_options.help.folder')
    )

# source image extention
input_options.add_argument(
    '-se',
    '--src-ext',
    type=str,
    default=user_dict[ConfigKeys.SRC_EXT.value],
    # choices=['.jpg', '.png', '.webp', '.jpeg', '.bmp'],
    required=False,
    help=lang.t('shell.args.input_options.help.ext')
    )

# recursive search
input_options.add_argument(
    '-r',
    '--recursive',
    action='store_true',
    default=user_dict[ConfigKeys.RECURSIVE.value],
    help=lang.t('shell.args.input_options.help.recursive')
    )

# source images
input_options.add_argument(
    '-si',
    '--src-images',
    type=str,
    nargs="+",
    required=False,
    help=lang.t('shell.args.input_options.help.images')
    )

output_options = parser.add_argument_group()
output_options.title =lang.t('shell.args.output_options.title')
output_options.description =lang.t('shell.args.output_options.description')

# destiny folder
output_options.add_argument(
    '-df',
    '--dst-folder',
    type=str,
    default=user_dict[ConfigKeys.DST_FOLDER.value],
    required=False,
    help=lang.t('shell.args.output_options.help.folder')
    )

# destiny image extention
output_options.add_argument(
    '-de',
    '--dst-ext',
    type=str,
    default=user_dict[ConfigKeys.DST_EXT.value],
    required=False,
    help=lang.t('shell.args.output_options.help.ext')
    )

# keep image organization
output_options.add_argument(
    '-k',
    '--keep-tree',
    action='store_true',
    default=user_dict[ConfigKeys.KEEP_TREE.value],
    help=lang.t('shell.args.output_options.help.keep_tree')
    )

# quality
output_options.add_argument(
    '-q',
    '--quality',
    type=int,
    default=user_dict[ConfigKeys.QUALITY.value],
    required=False,
    help=lang.t('shell.args.output_options.help.quality')
    )

# overwrite
output_options.add_argument(
    '-o',
    '--overwrite',
    action='store_true',
    default=user_dict[ConfigKeys.OVERWRITE.value],
    help=lang.t('shell.args.output_options.help.overwrite')
    )

if __name__=="__main__":

    # help reading in program
    # parser.print_help()

    # arguments reading
    args = parser.parse_args()
    print(args)


    # forcing input values
    # print(parser.parse_args(['-kr', '-de', '.png', '-df','.']))