# Image Converter

This software converts input image to the desired format extention
in the destiny folder chosen by the user.
It also admits compresssion options.

Written in Python and Pillow. 

## Features

Some of the implemented features:

- format extention selectable by user;
- single and recursive folder exploration;
- cloned subfolder tree and organization in output;
- compression adjustable by user;
- 4th image channel (*albedo*) erasing.


## Requirements

- Python 3
- Bash or equivalent shell.


## Installation



### Windows


```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```


### Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Usage and options

So far it's can only be used with Python interpreter:

```bash
py main.py <options>
```



### Source options

The easier way to work is searching images by file extention in a specified folder:


|short | long | explanation | default value|
|---|----|---|---|
|`-sf`|`--src-folder`| source folder's path|`.` |
|`-se`|`--src-ext`| source image's extention|`.webp`|
|`-r`|`--recursive`| recursive image search in source folder | disabled |

The alternative way by a list of image paths, in that case the other input options are disabled.

|short | long | explanation | 
|---|----|---|
|`-si`|`--src-images`| image list|

### Output options

The available options for output images are:

|short | long | explanation | default value| 
|---|----|---|---|
|`-df`|`--dst-folder`|destination folder's path|`converted-images` folder inside user directory |
|`-de`|`--dst-ext`|destination image's extention|`.jpg`|
|`-k`|`--keep-tree`| keep input folder's tree at output (only for recursive search)| disabled |
|`-q`|`--quality`| image quality   |`95`| 

Quality option enables output image compression but degrading image. By default is 95 (very slow losses / lossless). It can be between 1 and 100.


**Hint:** JPG images are very good for portraits, landscapes and drawings. Alternatively, PNG images are very good for technical schemas, diagrams, window screenshots, etc.


### Generic options


|short | long | explanation | 
|---|----|---|
|`-h`|`--help`| command line help |
|`-v`|`--version`| version tag|

## Examples


Command line help:

```bash
python main.py --help
```

Converting particular images to `.jpg` - all to same folder:

```bash
python main.py --src-image img1.webp img2.png ... --dst-folder output/ 
```

Recursive search of `.webp` images - keeping folder structure:

```bash
python main.py --src-folder examples/ --dst-folder output/ -r -k
```

Adding image compression to output images:

```bash
python main.py --src-folder examples/ --dst-folder output/ -r -k --quality 50 
```

Single search - input `.bmp` images, output images as `.png`:

```bash
python main.py --src-folder examples/ --dst-folder output/  -src-ext .bmp  -dst-ext .png  
```


