from pathlib import Path


images_ext = [
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tiff",
]


def images_search(
    directory: str, extentions: list[str] = images_ext, recursive: bool = False
):
    """Searchs for image files in the chosen folder.
    Returns a list of 'pathlib.Path' objects with the file paths found.
    It searchs extentions with lowercase and upercase together: .webp and .WEBP, .png and .PNG, ect.
    """
    images_list = []

    for ext in extentions:
        # recursive search
        images_found = ext_search(directory, ext, recursive)
        images_list.extend(images_found)

    return images_list


def ext_search(directory: str, extention: str, recursive: bool = False) -> list:
    """Searchs for files with the specified extention in the chosen folder.
    Returns a list of 'pathlib.Path' objects with the file paths found.
    It searchs extentions with lowercase and upercase together: .webp and .WEBP, .png and .PNG, ect.
    """

    # extention asked by user as search pattern
    pattern = f"*{extention}"
    # extentions in lowercase: .jpg, .webp, .png
    lower_pattern = pattern.lower()
    # extentions in uppercase: .JPG, .WEBP, .PNG
    upper_pattern = pattern.upper()

    # search for files to convert
    if recursive:
        # search with both extentions
        lower_paths = Path(directory).rglob(lower_pattern)
        upper_paths = Path(directory).rglob(upper_pattern)

    else:
        # search with both extentions
        lower_paths = Path(directory).glob(lower_pattern)
        upper_paths = Path(directory).glob(upper_pattern)

    # both lists are joined
    paths = list(lower_paths)
    paths.extend(list(upper_paths))

    # returns all file's paths found
    return paths


def relocate_path(
    src_path, dst_dir, dst_ext, src_parent_folder: str | None = None
) -> Path:
    """Adapt the input path to the output directory and the chosen extention.
    If the parent folder is 'None' only the filename will be adapted to output directory.
    """

    # creating destiny path
    src_path = Path(src_path)
    if src_parent_folder is None:
        # all the filenames will be together
        dst_name = src_path.name
        dst_path = Path(dst_dir).joinpath(dst_name)

    else:
        # original directory's tree replicated
        dst_subpath = src_path.relative_to(src_parent_folder)
        dst_path = Path(dst_dir).joinpath(dst_subpath)

    # new extention for filename
    dst_path = dst_path.with_suffix(dst_ext)
    return dst_path
