# standard libraries
from time import time
from pathlib import Path
from multiprocessing import Process

# packages
import psutil

# local module
from code import parser
from code import process_task


def main(dict_args: dict)->bool:
    """Image search, delivery and parallel processing in the same function.
    Returns 'True' if images were found, counter case returns 'False'"""

    # quality as percent
    quality = dict_args['quality']

    # original images organization 
    keep_organization = dict_args['keep_organization']

    # recursive search
    recursive = dict_args['recursive']

    # source folder and extention
    src_dir: str = dict_args['src_folder']
    src_ext: str = dict_args['src_ext']

    # image list
    src_list: list[str] = dict_args['src_images'] 

    # destiny folder and extention
    dst_dir: str = dict_args['dst_folder']
    dst_ext: str = dict_args['dst_ext']


    if src_list == None or len(src_list) == 0: 

        # search for images to convert
        pattern = f"*{src_ext}"

        if recursive:
            src_paths = Path(src_dir).rglob(pattern)
            print("Recursive search - enabled")
        else:
            src_paths = Path(src_dir).glob(pattern)
            print("Single folder search - by default")

        src_paths = list(src_paths)
        nro_images = len(src_paths)

        print(f"Converting images from folder: {src_dir}")
        print(f"Source image extention: {src_ext}")
        print(f"Images found: {nro_images}")
        
        if nro_images == 0:
            return False

        if keep_organization:
            print("Keeping folder's organization.")
            src_folder = Path(src_dir)
        else:
            print("All output images in the output directory.")
            src_folder = None

    else:
        
        # image list from arguments
        src_paths = src_list
        nro_images = len(src_paths)
        
        print("Converting images from input:")
        for image in src_list:
            print(image)


        print(f"Images: {nro_images}")

        if nro_images == 0:
            return False
            
        print("All output images in the output directory.")
        src_folder = None


    # create destiny folder if it doesn't exists
    if Path(dst_dir).is_dir():
        print(f"Folder already exists: {dst_dir}")

    else:
        print(f"Creatign folder in {dst_dir}")
        Path(dst_dir).mkdir(
            parents=True
            )

    print(f"Output image extention: {dst_ext}")

    # image delivery in multiple cores  
    cores = psutil.cpu_count(logical=False)
    print(f"CPU physical cores detected: {cores}")
    proccess_lists = []

    for c in range(cores):

        paths = src_paths[ c : nro_images: cores]
        args = (paths, dst_dir, dst_ext, src_folder, quality)      
        procc = Process(target=process_task, args=args) 
        procc.daemon = True
        procc.start()
        proccess_lists.append(procc)


    # await until all proccess finishes
    for procc in proccess_lists:
        procc.join()

    return True


parser.version = '1.1.1'

# arguments reading
input_args = parser.parse_args()

# arguments convertion
dict_args = vars(input_args)


start = time()

images_found = main(dict_args=dict_args)

end = time()

if images_found:

    print(f"Elapsed time: {(end-start)*1000 :7.6} mseg")

else:

    print("No images found - Cancelled")