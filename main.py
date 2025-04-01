from time import time
from pathlib import Path

from PIL import Image



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


for path in src_paths:

    # creating destiny path
    src_path = Path(path).with_suffix(dst_ext)
    dst_name = src_path.name
    dst_path = Path(dst_dir).joinpath(dst_name)

    # converting image
    im = Image.open(path)
    im.save(dst_path, quality=quality)


end = time()

print(f"Elapsed time: {(end-start)*1000 :7.6} mseg")
