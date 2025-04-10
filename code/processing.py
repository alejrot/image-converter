from pathlib import Path
from threading import Thread
from multiprocessing import Value, Event, Lock

# packages
from PIL import Image
from rich.progress import Progress
from rich import print
import psutil

# project code
from code.paths import relocate_path


# sync and global elements
folder_lock = Lock()

processed_counter = Value('i', 0)
processed_event   = Event()



def processed_bar(total_count:int):
    """Shows a progress bar showing how many images were processed."""
    global processed_counter
    with Progress() as progress:

        task = progress.add_task("[green]Processing...", total=total_count)

        while not progress.finished:
            # bar remains blocked until a new image is converted
            processed_event.wait()
            # updates progress bar
            i = processed_counter.value
            progress.update(task, completed=i)
            # locks the progress again
            processed_event.clear()



def convert_image(src_path, dst_path, quality:int=95):
    """This thread saves the source image in the destiny path after its conversion.
    Quality is a percentage that defines compression: a high percentage means minimal quality loss.
    If source image is 4-channel (RGBA) then the output will be converted to 3-channel (RGB). 
    """

    try:
        # RGB and monochrome images are converted directly
        with Image.open(src_path) as im:
            im.save(dst_path, quality=quality)

    except:
        # RGBA saving throws exception 
        with Image.open(src_path) as im:    
            # RGBA images are converted deleting transparency channel
            source = im.split()
            if len(source) == 4:
                r,g,b,a = source
                # A channel discarded
                im = Image.merge("RGB", (r,g,b))
                im.save(dst_path, quality=quality)
                # print(f"Image: {src_path} - transparency channel discarded")
            else:
                print(f"Image: {src_path} - unsupported image")
    
    finally:
        
        # Orders the progress bar counter and update it
        processed_counter.value += 1
        processed_event.set()



def process_task(src_paths, dst_dir, dst_ext, src_parent_folder:str|None=None, quality:int=95):
    """This task creates a thread for each image to convert and awaits until finish. 
    """

    threads_list = []

    for src_path in src_paths:

        # creating destiny path
        dst_path = relocate_path(src_path, dst_dir, dst_ext, src_parent_folder)

        # images subfolders are created if it doesn't exist
        subfolder = dst_path.parent
        # the lock is to prevent unlikely but possible folder overwrite and program crash
        folder_lock.acquire()
        if subfolder.is_dir()==False:
            subfolder.mkdir(parents=True)
        folder_lock.release()

        # converting images in parallel
        args = (src_path, dst_path, quality,)
        conv_thread = Thread(
            target=convert_image,
            args  =args
            ) 

        conv_thread.start()
        threads_list.append(conv_thread)

        # limit maximum parallell threads per proccess
        h = psutil.cpu_count(logical=True)/psutil.cpu_count(logical=False)

        if len(threads_list) > h:
            # awaits until first thread end and discards it
            thread = threads_list[0]
            thread.join()
            threads_list.remove( thread)
            # if other threads have ended they are discarded too
            alive_obj = filter(lambda x: x.is_alive(), threads_list)
            threads_list = list(alive_obj)
            

    # awaits for all image conversion's end
    for thread in threads_list:
        thread.join()