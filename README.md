# Image Converter

This software converts input image
to the desired format extension
in the destiny folder chosen by the user.
It also admits compresssion options.

Written in Python and Pillow. 

## Features

Some of the implemented features:

- format extension selectable by user;
- single and recursive folder exploration;
- cloned subfolder tree and organization in output;
- compression adjustable by user;
- 4th image channel (*albedo*) erasing (by *default*).


## Requirements

- Python 3
- Bash or equivalent shell.


## Installation


<details>
<summary>
Windows
</summary>



```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

</details>

<details>
<summary>
Linux
</summary>

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
</details>


## Usage and options

So far it's can only be used with Python interpreter:

```bash
py main.py <arguments> 
```

<details>
<summary>
Source options
</summary>

The easier way to work is searching images by file extension in a specified folder:


|short | long | explanation | default value|
|---|----|---|---|
|`-sf`|`--src-folder`| source folder's path|`.` |
|`-se`|`--src-ext`| source image's extension|`ALL`|
|`-r`|`--recursive`| recursive image search in source folder | disabled |

`ALL` or `all` wildcard enables image searching of any allowed format.
The alternative way by a list of image paths, in that case the other input options are disabled.

|short | long | explanation | 
|---|----|---|
|`-si`|`--src-images`| image list|

</details>


<details>
<summary>
Output options
</summary>

The available options for output images are:

|short | long | explanation | default value| 
|---|----|---|---|
|`-df`|`--dst-folder`|destination folder's path|`converted-images` folder inside user directory |
|`-de`|`--dst-ext`|destination image's extension|`.jpg`|
|`-k`|`--keep-tree`| keep input folder's tree at output (only for recursive search)| disabled |
|`-o`|`--overwrite`| Forces conversion if output images already exists | disabled |
|`-q`|`--quality`| image quality (as percent number)  |`95`| 

Quality option enables output image compression but degrading image. By default is 95 (very slow losses).
It can be between 1 and 100;
however not all formats can be compressed (see [Annex](#appendix-image-formats)).

</details>


<details>
<summary>
Generic options
</summary>


|short | long | explanation | 
|---|----|---|
|`-h`|`--help`| command line help |
|`-v`|`--version`| version tag|

</details>



## Examples

<details>
<summary>
Command line help:
</summary>

```bash
python main.py --help
```
</details>


<details>
<summary>
Converting particular images to JPG - all to same folder:
</summary>

```bash
python main.py --src-image img1.webp img2.png ... --dst-folder output/ 
```


</details>

<details>
<summary>
Recursive search of WEBP images - keeping folder structure:
</summary>

```bash
python main.py --src-folder examples/ --dst-folder output/ -r -k
```
</details>

<details>
<summary>
Adding image compression to output images:
</summary>

```bash
python main.py --src-folder examples/ --dst-folder output/ -r -k --quality 50 
```
</details>

<details>
<summary>
Single search - input BMP images, output images as PNG:
</summary>

```bash
python main.py --src-folder examples/ --dst-folder output/  -src-ext .bmp  -dst-ext .png  
```
</details>


## Appendix: image formats


### JPG

JPG images are very good for portraits, landscapes and drawings.
Some of its properties:
 
- lossy format image;
- supports image compression;
- widely used and highly compatibility.


### PNG

PNG images are very good for technical schemas, diagrams, window screenshots, etc;
however is often used for portraits, landscapes and drawings.
Some of its properties:

- lossless format image;
- doesn't support image compression;
- supports 4th channel image (*albedo*).
- widely used and highly compatibility.

**Warning:** PNG diagrams could be degraded when are converted to other formats,
specially colours could be changed.


### WEBP

WEBP is a newer image format trying to overcome JPG and PNG formats.
Some of its properties:

- supports lossless and lossy image compression;
- better quality image and lower space disk than JPG at high compression rates (*lossy*);
- lower image size than PNG with *lossless* compression - around 25% less;
- supports 4th channel image (*albedo*).
- not so extended use and compatibility as JPG and PNG but rising.


This program **only does lossy** compression during conversion.

