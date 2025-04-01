from time import time
from pathlib import Path
from multiprocessing import Process
from threading import Thread

import psutil
from PIL import Image


def thread_convert_image(src_path, dst_path, quality:int=95):
    """This thread saves the source image in the destiny path after its conversion.
    Quality is a percentage that defines compression: a high percentage means minimal quality loss.
    """
    # conversion with Pillow
    im = Image.open(src_path)
    im.save(dst_path, quality=quality)


def process_task(src_paths, dst_dir, dst_ext):
    """This task creates a thread for each image to convert and awaits until finish. 
    """

    threads_list = []

    for path in src_paths:

        # creating destiny path
        src_path = Path(path).with_suffix(dst_ext)
        dst_name = src_path.name
        dst_path = Path(dst_dir).joinpath(dst_name)

        # converting images in parallel
        args = (path, dst_path, quality,)
        conv_thread = Thread(
            target=thread_convert_image,
            args  =args
            ) 

        conv_thread.start()
        threads_list.append(conv_thread)

    # awaits for conversion's end
    for thread in threads_list:
        thread.join()


# quality as percent
quality = 95

# source folder and extention
src_dir: str = "examples/"
src_ext: str = "*.webp"


# destiny folder and extention
# dst_dir: str = "output/"
dst_dir: str = "/dev/shm/image-converter/"   # RAM memory (only in Linux)
dst_ext: str = ".jpg"

# create destiny folder if it doesn't exists
if Path(dst_dir).is_dir():
    print(f"folder already exists: {dst_dir}")

else:
    print(f"creatign folder in {dst_dir}")
    Path(dst_dir).mkdir(
        parents=True
        )


start = time()

# search of images to convert
pattern=f"*{src_ext}"
src_paths = Path(src_dir).rglob(pattern)
src_paths = list(src_paths)

cores = psutil.cpu_count(logical=False)
print(f"Physical cores detected: {cores}")

nro_images = len(src_paths)
n = nro_images // cores
print(f"Images found: {nro_images}")

proccess_lists = []

# image delivery in multiple cores  
for c in range(cores):

    m = c*n
    paths = src_paths[ m : m+n ]

    args = (paths, dst_dir, dst_ext,)      
    procc = Process(target=process_task, args=args) 
    procc.start()

    proccess_lists.append(procc)


# await until all proccess finishes
for procc in proccess_lists:
    procc.join()


end = time()

print(f"Elapsed time: {(end-start)*1000 :7.6} mseg")

