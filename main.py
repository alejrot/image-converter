# standard libraries
from time import time
from pathlib import Path
from multiprocessing import Process
from threading import Thread

# packages
import psutil
from rich import print
from rich.progress import Progress

# local module
from code import parser
from code import process_task
from code import ext_search
from code import processed_bar



def main(dict_args: dict)->bool:
    """Image search, delivery and parallel processing in the same function.
    Returns 'True' if images were found, counter case returns 'False'"""

    # quality as percent
    quality = dict_args['quality']

    # original images organization 
    keep_tree = dict_args['keep_tree']

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


    print("[green]Input options:")

    if src_list == None or len(src_list) == 0: 



        if recursive:
            print("[yellow]Recursive search enabled")
        else:
            print("[yellow]Single search")

        print(f"[blue]Sorce folder: [yellow]{src_dir}")
        print(f"[blue]Image extention: [yellow]{src_ext}")

        src_paths = []
        nro_images = 0

        with Progress() as progress:

            task_bar = progress.add_task("[green]Searching...", total=100, start=False)

            # search for images to convert
            src_paths = ext_search(src_dir, src_ext, recursive)

            progress.update(task_bar, completed=100)

            src_paths = list(src_paths)
            nro_images = len(src_paths)


        print(f"[blue]Images found: [yellow]{nro_images}")
        
        if nro_images == 0:
            return False

        print("[green]Output options:")

        if keep_tree:
            print("[yellow]Keeping folder's organization in output.")
            src_folder = Path(src_dir)
        else:
            print("[yellow]All output images in the output directory.")
            src_folder = None

    else:
        
        # image list from arguments
        src_paths = src_list
        nro_images = len(src_paths)

        print("[yellow]Converting images from input:")

        print(f"[blue]Images provided: [yellow]{nro_images}")

        if nro_images == 0:
            return False
            
        print("[green]Output options:")

        print("[blue]All output images in the output directory.")
        src_folder = None


    # create destiny folder if it doesn't exists
    if Path(dst_dir).is_dir():
        print(f"[blue]Destination folder already exists: [yellow]{dst_dir}")

    else:
        print(f"[blue]Creatign destination folder in [yellow]{dst_dir}")
        Path(dst_dir).mkdir(
            parents=True
            )

    print(f"[blue]Output image extention: [yellow]{dst_ext}")

    # shows progress bar - parallel proccess
    bar_procc = Process(target=processed_bar, args=(nro_images,)) 
    bar_procc.daemon = True
    bar_procc.start()

    # image delivery in multiple proccess, each one with multiple threads
    proccess_lists = []
    cores = psutil.cpu_count(logical=False)

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


parser.version = '1.2.0'

# arguments reading
input_args = parser.parse_args()

# arguments convertion
dict_args = vars(input_args)

# required in Windows and Pyinstaller 
if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()

    start = time()

    images_found = main(dict_args=dict_args)

    end = time()

    if images_found:

        print(f"Elapsed time: {(end-start)*1000 :7.6} mseg")

    else:

        print("No images found - Cancelled")