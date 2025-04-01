from time import time
from pathlib import Path

from multiprocessing import Pool
from threading import Thread

import psutil


from PIL import Image



import cv2



def thread_convert_image(src_path, dst_path, quality):

    print(f"{src_path}")

    # PILLOW
    im = Image.open(src_path)
    im.save(dst_path, quality=quality)

    # # OPENCV
    # img = cv2.imread(src_path)
    # guardado_exitoso = cv2.imwrite(dst_path, img)
    # del img



# quality as percent
quality = 95


# source folder and extention
src_dir: str = "examples/"
src_ext: str = "*.webp"


dst_dir: str = "output/"
dst_dir: str = "/dev/shm/"   # RAM memory (only in Linux)


dst_ext: str = ".jpg"


# search of images to copnvert
pattern=f"*{src_ext}"
src_paths = Path(src_dir).glob(pattern)
src_paths = list(src_paths)


start = time()


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


end = time()



print(f"Elapsed time: {(end-start)*1000 :7.6} mseg")




