# How to set up a shared LISA image annotation project

**Have not made a requirements file yet.**

## Select frames from videos
Videos were first uploaded to Research File Service. 
All frames were extracted from videos and saved in folders with the name of the video.

```
./extract-allframes2.sh \
  $ROOT/fish-tank-obstacles/data/zebrafish_videos/videos/ \
  /media/user/6363-3631/images/
```
*Script only looks for file type '.MP4' with capitals.* Change script (line 18) for other file types.

## Select frames from videos
The last step produces a large number of frames. We don't necessarily need to annotate all of them. 
A script was used to select a defined percent of the frames in each folder and compile these into a .txt file. 

Requires: list_sample_files.sh
Example usage: ./list_sample_files.sh "/path/to/directory" 10

```
./list_sample_files.sh "/Volumes/RFS/Triggerfish Navigation/Zebrafish/allframes" 10
```
## Move selected images to their own local folder
Folder selection is within the script.

```
python3 move-images-for-annoation.py
```
Images were saved here: Volumes/RFS/Triggerfish Navigation/Zebrafish/annotation/ but init-lisa-project.py does not like the space in the Triggerfish Navigation folder name so I moved the annotation to a local computer folder during processing.

## Upload images to a public server
Abhishek Dutta then uploaded images on https://meru.robots.ox.ac.uk
https://meru.robots.ox.ac.uk/dset/image/cait-newport/triggerfish-navigation/zebrafish/allframes/GX010499/f19689.jpg

## Create a LISA project .json file
Run: init-list-project.py
On my system, this required: 

* many packages need to be installed
* lisa.py
* Depending on the package version, you may get the following error: 
 " /AutoZebrafish/venv/lib/python3.12/site-packages/imma/dili.py", line 14, in <module>
    from collections import Mapping, Set, Sequence "
    To fix this:
    - open /Users/user/projects/AutoZebrafish/venv/lib/python3.12/site-packages/imma/dili.py
    - change line 14: "from collections import Mapping, Set, Sequence" to "from collections.abc import Mapping, Set, Sequence"

TODO: Make a Requirements file. Is it possible to make it just for this part of the project so it could be a stand-alone section? If so, also have it check if the lisa.py file exists.

Note: offset lets you skip images by an offset interval (e.g. offset=25 means you only take every 25th image)

```
# Example usage:
cd $ROOT/AutoZebrafish/tools

python3 init-lisa-project.py \
--image-dir=/Users/user/projects/AutoZebrafish/detector-training/ImageAnnotation/annotation/ \
--file-src-prefix=https://meru.robots.ox.ac.uk/dset/image/cait-newport/triggerfish-navigation/zebrafish/allframes/ \
--object-name=fish \
--offset=1 \
--outfn=/Users/user/projects/AutoZebrafish/training-data/1-frames-sel-for-annotation.json
```

## Test that this project works
Save the list.html file in the folder where the images are stored. 
In this case: /Users/user/projects/AutoZebrafish/detector-training/ImageAnnotation/annotation
This gets around a folder permissions issue. 

In a web browser, open: lisa.html
Use 'Load Existing Project' to select the 1-frames-sel-for-annotation.json 

You can stop at this stage and annotate images locally. 
**Remember to save your progress frequently**
When you save the annotations, the JSON file saves locally. Each time you save, you will overwrite the file.

## Create a shared project
To create a project that is stored on a server, continue to this part. 

Run: push-as-shared-project.py

```
python3 push-as-shared-project.py \
--lisa-fn=/Users/user/projects/AutoZebrafish/training-data/1-frames-sel-for-annotation.json
```
This will produce a shared project fid in the **terminal output**. Copy and paste this.
For example: 03c95628-780d-425d-a698-af2e0ad53d45

In a web browser, open: lisa.html
Use the 'Load Shared Project' box and put in the project fid. Select 'Load'.

If the images don't load, hit 'f' on your keyboard. A box will appear and you enter your server folder pathway.
For example: https://meru.robots.ox.ac.uk/dset/image/cait-newport/triggerfish-navigation/zebrafish/allframes/

I had an issue where I got an error after this process, but I opened LISA from a different folder and it worked. 

The annotations file will save on the server. Email Abhishek when you are done to get this. 
