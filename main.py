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
    try:
        # conversion with Pillow
        im = Image.open(src_path)
        im.save(dst_path, quality=quality)
    except:
        print(f"Image: {src_path} - unsupported image")




def process_task(src_paths, dst_dir, dst_ext, parent_folder:str|None=None):
    """This task creates a thread for each image to convert and awaits until finish. 
    """

    threads_list = []

    for path in src_paths:

        # creating destiny path
        src_path = Path(path)
        if parent_folder == None:
            # all the images will be created together
            dst_name = src_path.name
            dst_path = Path(dst_dir).joinpath(dst_name)
            # new extention for image
            dst_path = dst_path.with_suffix(dst_ext)
        else:
            # original directory's tree replicated
            dst_subpath = src_path.relative_to(parent_folder)
            dst_path = Path(dst_dir).joinpath(dst_subpath)
            # subfolder created if it doesn't exist
            subfolder = dst_path.parent
            if subfolder.is_dir()==False:
                subfolder.mkdir(parents=True)
            # new extention and path for image
            dst_path = dst_path.with_suffix(dst_ext)


        # converting images in parallel
        args = (path, dst_path, quality,)
        conv_thread = Thread(
            target=thread_convert_image,
            args  =args
            ) 
        conv_thread.start()
        threads_list.append(conv_thread)

    # awaits for all image conversion's end
    for thread in threads_list:
        thread.join()


# quality as percent
quality = 95

# original images organization 
keep_organization = True

# source folder and extention
src_dir: str = "examples/"
# src_ext: str = "*.webp"
src_ext: str = "*.png"


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


if keep_organization:
    src_folder = Path(src_dir)
else:
    src_folder = None

proccess_lists = []

# image delivery in multiple cores  
for c in range(cores):

    paths = src_paths[ c : nro_images: cores]

    args = (paths, dst_dir, dst_ext, src_folder)      
    procc = Process(target=process_task, args=args) 
    procc.daemon = True
    procc.start()

    proccess_lists.append(procc)


# await until all proccess finishes
for procc in proccess_lists:
    procc.join()


end = time()

print(f"Elapsed time: {(end-start)*1000 :7.6} mseg")

