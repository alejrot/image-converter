from time import time
from pathlib import Path

from multiprocessing import Process

import psutil

from code import input_args, process_task


# print(input_args)
dict_args = vars(input_args)




# quality as percent
quality = dict_args['quality']

# original images organization 
keep_organization = dict_args['keep_organization']

# source folder and extention
src_dir: str = dict_args['src_folder']
src_ext: str = dict_args['src_ext']
# dict_args['src_images']            # !!!

# destiny folder and extention
dst_dir: str = dict_args['dst_folder']
dst_ext: str = dict_args['dst_ext']

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
pattern = f"*{src_ext}"
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

    args = (paths, dst_dir, dst_ext, src_folder, quality)      
    procc = Process(target=process_task, args=args) 
    procc.daemon = True
    procc.start()

    proccess_lists.append(procc)


# await until all proccess finishes
for procc in proccess_lists:
    procc.join()


end = time()

print(f"Elapsed time: {(end-start)*1000 :7.6} mseg")

