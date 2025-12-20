"""This module is the responsible of converting images in different threads."""
from pathlib import Path
from multiprocessing import Value, Event, Lock
from concurrent.futures import ThreadPoolExecutor

# project code
from .paths import relocate_path

# packages
from PIL import Image
from rich import print as print


# sync and global elements
folder_lock = Lock()

processed_counter = Value("i", 0)
processed_event = Event()



def convert_image(src_path, dst_path, quality: int = 95):
    """This thread saves the source image in the destiny path after its conversion.
    Quality is a percentage that defines compression: a high percentage means minimal quality loss.
    If source image is 4-channel (RGBA) then the output will be converted to 3-channel (RGB).
    If source image has more of a frame then the output wil be cloned.
    """

    try:
        # RGB and monochrome images are converted directly
        with Image.open(src_path) as im:

            source = im.split()
            # print(f"channels: {len(source)}, mode: {im.mode}, image: {src_path}")
            
            if hasattr(im, 'n_frames'):
                # animated images are NOT compressed
                if im.n_frames > 1:
                    # images are only copied
                    bytes_string = Path(src_path).read_bytes()
                    Path(dst_path).write_bytes(bytes_string)
                    del bytes_string, source
                    print(f"[bold yellow]Image: [green]{src_path} [bold yellow] is multiframe image - not converted")
                    return
                
            if len(source) == 4:
                # Albedo ('a') channel discarded
                r, g, b, _ = source
                im = Image.merge("RGB", (r, g, b))
                im.save(dst_path, quality=quality)
                # print(f"Image: {src_path} - transparency channel discarded")
                del r, g, b, _
                del source
                return

            #  1-channel images case
            elif len(source) == 1:
                # print(f"[bold cyan]    1 channel image ")
                im.save(dst_path, quality=quality)
                del source
                return

            #  3-channel images case
            else:
                im.save(dst_path, quality=quality)
                del source
                return


    except Exception as exception_message:

        # RGBA saving throws exception
        print(f"[bold red]Exception: {exception_message}")
        print(f"[bold red]Image: [bold yellow]{src_path}")
        print(f"[bold red]Mode:  [bold yellow]{im.mode}")
        return


    finally:
        # Orders the progress bar counter and update it
        processed_counter.value += 1
        processed_event.set()
        return


def image_threads(
    src_paths, dst_dir, dst_ext, src_parent_folder: str | None = None, quality: int = 95
):
    """This task creates a thread for each image to convert and awaits until finish."""

    # thread pool for processing tasks
    executor = ThreadPoolExecutor()

    for src_path in src_paths:
        # creating destiny path
        dst_path = relocate_path(src_path, dst_dir, dst_ext, src_parent_folder)

        # images subfolders are created if it doesn't exist
        subfolder = dst_path.parent
        # the lock is to prevent unlikely but possible folder overwrite and program crash
        folder_lock.acquire()
        if not subfolder.is_dir():
            subfolder.mkdir(parents=True)
        folder_lock.release()

        # converting images in parallel
        executor.submit(
            convert_image,
            src_path,
            dst_path,
            quality,
            )

    # threads pool close
    executor.shutdown()

