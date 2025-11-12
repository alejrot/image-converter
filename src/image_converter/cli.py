# standard libraries
from pathlib import Path
from threading import Thread
from argparse import ArgumentParser
from copy import deepcopy

# packages
from rich import print as print
from rich.progress import Progress

# local module
from .processing import image_threads, processed_counter, processed_event
from .paths import ext_search, relocate_path, images_ext
from .lang import lang


def processed_bar(total_count: int):
    """Shows a progress bar showing how many images were processed."""
    # global processed_counter
    with Progress() as progress:
        task = progress.add_task(
            f"[green]{lang.t('shell.main.search.start')}", total=total_count
        )

        while not progress.finished:
            # bar remains blocked until a new image is converted
            processed_event.wait()
            # updates progress bar
            i = processed_counter.value
            progress.update(task, completed=i)
            # locks the progress again
            processed_event.clear()


def cli_process(args: ArgumentParser) -> bool:
    """Image search, delivery and parallel processing in the same function.
    Returns 'True' if images were found, counter case returns 'False'"""

    # quality as percent
    quality = args.quality

    # original images organization
    keep_tree = args.keep_tree

    # recursive search
    recursive = args.recursive

    # overwrite old files
    overwrite = args.overwrite

    # source folder and extention
    src_dir: str = args.src_folder
    src_ext: str = args.src_ext

    src_dir = str(Path(src_dir).expanduser())

    # image list
    src_list: list[str] = args.src_images

    # destiny folder and extention
    dst_dir: str = args.dst_folder
    dst_ext: str = args.dst_ext

    dst_dir = Path(dst_dir).expanduser()
    dst_dir = str(dst_dir)

    print(f"[green]{lang.t('shell.main.input_options')}")

    if src_list is None or len(src_list) == 0:
        if recursive:
            print(f"[yellow]{lang.t('shell.main.recursive.enabled')}")
        else:
            print(f"[yellow]{lang.t('shell.main.recursive.disabled')}")

        print(f"[blue]{lang.t('shell.main.search.folder')} [yellow]{src_dir}")

        print(f"[blue]{lang.t('shell.main.search.ext')} [yellow]{src_ext}")

        # search for images to convert
        src_paths = []
        nro_images = 0

        with Progress() as progress:
            task_bar = progress.add_task(
                f"[green]{lang.t('shell.main.search.start')}", total=100, start=False
            )

            if src_ext.upper() == "ALL":
                exts = deepcopy(images_ext)
                for ext in exts:
                    src_paths.extend(ext_search(src_dir, ext, recursive))
            else:
                src_paths.extend(ext_search(src_dir, src_ext, recursive))

            progress.update(task_bar, completed=100)
            src_paths = list(src_paths)
            nro_images = len(src_paths)

        print(f"[blue]{lang.t('shell.main.search.end')} [yellow]{nro_images}")
        if nro_images == 0:
            return False

        print(f"[green]{lang.t('shell.main.output.section')}")

        if keep_tree:
            print(f"[yellow]{lang.t('shell.main.keep_tree.enabled')}")
            src_folder = Path(src_dir)
        else:
            print(f"[yellow]{lang.t('shell.main.keep_tree.disabled')}")
            src_folder = None

    else:
        # image list from arguments
        src_paths = src_list
        nro_images = len(src_paths)

        print(f"[yellow]{lang.t('shell.main.images.intro')}")
        print(f"[blue]{lang.t('shell.main.images.input')} [yellow]{nro_images}")
        if nro_images == 0:
            return False

        print(f"[green]{lang.t('shell.main.output.section')}")

        print(f"[blue]{lang.t('shell.main.keep_tree.disabled')}")
        src_folder = None

    print(f"[blue]{lang.t('shell.main.output.ext')} [yellow]{dst_ext}")

    if not overwrite:
        # discarding paths of images already converted or preexistent in output
        print(f"[yellow]{lang.t('shell.main.overwrite.disabled')}")

        discarded_counter = 0
        unconverted_images = []

        for src_image in src_paths:
            output_image = relocate_path(src_image, dst_dir, dst_ext, src_folder)

            if output_image.exists():
                discarded_counter += 1

            else:
                unconverted_images.append(src_image)

        print(
            f"[blue]{lang.t('shell.main.overwrite.repeated')} [yellow]{discarded_counter}"
        )

        src_paths = unconverted_images
        nro_images = len(src_paths)

        print(f"[blue]{lang.t('shell.main.overwrite.pending')} [yellow]{nro_images}")

        if nro_images == 0:
            return False

    else:
        # converting all input images
        print(f"[yellow]{lang.t('shell.main.overwrite.enabled')}")

    # create destiny folder if it doesn't exists
    if Path(dst_dir).is_dir():
        print(f"[blue]{lang.t('shell.main.output.folder.exists')} [yellow]{dst_dir}")

    else:
        print(f"[blue]{lang.t('shell.main.output.folder.create')} [yellow]{dst_dir}")
        Path(dst_dir).mkdir(parents=True)

    # the progress  bar has its own thread
    bar_thread = Thread(
        target=processed_bar,
        args=(len(src_paths),),
    )

    bar_thread.start()

    # image delivery in multiple threads
    # it also shows progress bar
    image_threads(src_paths, dst_dir, dst_ext, src_folder, quality)

    return True
