from pathlib import Path
from threading import Thread

# conversion with Pillow
from PIL import Image


def thread_convert_image(src_path, dst_path, quality:int=95):
    """This thread saves the source image in the destiny path after its conversion.
    Quality is a percentage that defines compression: a high percentage means minimal quality loss.
    If source image is 4-channel (RGBA) then the output will be converted to 3-channel (RGB). 
    """
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
                # im.save("9dzign_flame.jpg", quality=quality)
                im.save(dst_path, quality=quality)
                print(f"Image: {src_path} - transparency channel discarded")
            else:
                print(f"Image: {src_path} - unsupported image")



def process_task(src_paths, dst_dir, dst_ext, parent_folder:str|None=None, quality:int=95):
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