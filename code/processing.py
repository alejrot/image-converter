from pathlib import Path
from threading import Thread, Lock

# conversion with Pillow
from PIL import Image

# project code
from code.paths import relocate_path

folder_lock = Lock()

def thread_convert_image(src_path, dst_path, quality:int=95):
    """This thread saves the source image in the destiny path after its conversion.
    Quality is a percentage that defines compression: a high percentage means minimal quality loss.
    If source image is 4-channel (RGBA) then the output will be converted to 3-channel (RGB). 
    """

    # image subfolders are created if it doesn't exist
    subfolder = dst_path.parent
    # the lock is to prevent unlikely but possible folder overwrite and program crash
    folder_lock.acquire()
    if subfolder.is_dir()==False:
        subfolder.mkdir(parents=True)
    folder_lock.release()

    try:
        with Image.open(src_path) as im:
            # RGB and monochrome images are converted directly
            im.save(dst_path, quality=quality)

    except:
        with Image.open(src_path) as im:    
            # RGBA images are converted deleting transparency channel
            source = im.split()
            if len(source) == 4:
                r,g,b,a = source
                # A channel discarded
                im = Image.merge("RGB", (r,g,b))
                im.save(dst_path, quality=quality)
                print(f"Image: {src_path} - transparency channel discarded")
            else:
                print(f"Image: {src_path} - unsupported image")



def process_task(src_paths, dst_dir, dst_ext, src_parent_folder:str|None=None, quality:int=95):
    """This task creates a thread for each image to convert and awaits until finish. 
    """

    threads_list = []

    for src_path in src_paths:

        # creating destiny path
        dst_path = relocate_path(src_path, dst_dir, dst_ext, src_parent_folder)

        # converting images in parallel
        args = (src_path, dst_path, quality,)
        conv_thread = Thread(
            target=thread_convert_image,
            args  =args
            ) 
        conv_thread.start()
        threads_list.append(conv_thread)

    # awaits for all image conversion's end
    for thread in threads_list:
        thread.join()