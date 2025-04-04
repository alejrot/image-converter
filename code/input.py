
import argparse

from code.consts import Default

program_name = "image-converter"
version = '0.0'



# new arguments parser
parser = argparse.ArgumentParser(
    prog=program_name,
    # usage='%(prog)s [options]',
    usage=f'{program_name} [options]',
    description='Converts the input images to the chosen extention.',
    # epilog='Text at the bottom of help',
    )
    

parser.version = version

# program version
parser.add_argument(
    '-v',
    '--version',
    action='version',
    )
    
source_type = parser.add_argument_group()
source_type.title = "Input options"
source_type.description = "Chooses image's source between a folder's path and an image path's list."


# source images
source_type.add_argument(
    '-si',
    '--src-images',
    type=str,
    nargs="+",
    required=False,
    help="Source image's list."
    )


# source folder
source_type.add_argument(
    '-sf',
    '--src-folder',
    type=str,
    default=Default.SRC_FOLDER.value,
    required=False,
    help=f"Source folder's path. Images will be searched there. By default is {Default.SRC_FOLDER.value}"
    )

# source image extention
source_type.add_argument(
    '-se',
    '--src-ext',
    type=str,
    default=Default.SRC_EXT.value,
    # choices=['.jpg', '.png', '.webp', '.jpeg', '.bmp'],
    required=False,
    help=f"Image's extention to be searched and converted. Values: '.bmp', '.webp', ect. By default is {Default.SRC_EXT.value}."
    )


output_options = parser.add_argument_group()
output_options.title = "Output options"
output_options.description = "Changes output properties: output folder, extention and quality."

# quality
output_options.add_argument(
    '-q',
    '--quality',
    type=int,
    default=Default.QUALITY.value,
    required=False,
    help=f'Quality percent. Higher quality means less losses but hight file size. By default is {Default.QUALITY.value}.'
    )

# destiny folder
output_options.add_argument(
    '-df',
    '--dst-folder',
    type=str,
    default=Default.DST_FOLDER.value,
    required=False,
    help=f"Destiny folder's path. By default is {Default.DST_FOLDER.value}"
    )

# destiny image extention
output_options.add_argument(
    '-de',
    '--dst-ext',
    type=str,
    default=Default.DST_EXT.value,
    choices=['.jpg', '.png', '.webp', '.jpeg', '.bmp'],
    required=False,
    help=f"Desired image's extention. Values: '.jpg', '.png', ect. By default is {Default.DST_EXT.value}."
    )


recursive_options = parser.add_argument_group()
recursive_options.title = "Search options" 
recursive_options.description = "Enables recursive search and output folder's delivery."

# recursive search
recursive_options.add_argument(
    '-r',
    '--recursive',
    action='store_true',
    help="Enables the recursive search in source folder. By default is 'False'."
    )

# keep image organization
recursive_options.add_argument(
    '-k',
    '--keep-tree',
    action='store_true',
    help="Replies the folder's source image organization at output. Only works in recursive searching."
    )



if __name__=="__main__":

    # help reading in program
    # parser.print_help()

    # arguments reading
    args = parser.parse_args()
    print(args)


    # forcing input values
    # print(parser.parse_args(['-kr', '-de', '.png', '-df','.']))