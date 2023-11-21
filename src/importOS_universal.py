import os
import shutil
import time as t
from pathlib import Path

# get the source directory from user input
src_directory = 'C:\\Users\\norppa\\nerdCorner\\input for sorter' #str(input("Source directory: "))
src = Path(src_directory).expanduser()

# use os.path.expanduser() to handle ~ in the path
dst_directory = str(input("Destination directory: "))
dst_directory = os.path.expanduser(dst_directory)

# check if the destination directory exists before creating it
if not os.path.exists(dst_directory):
    os.makedirs(dst_directory)

# copy the contents of the source directory directly into the destination directory (update this comment)
    # create folders for the files to be put in (?)
for item in src.glob('*'):

    # get the creation and modification datetime of the file
    creation_time = os.path.getctime(item)
    modification_time = os.path.getmtime(item)

    # convert the timestamps to datetime objects
    creation_datetime = t.ctime(creation_time)
    modification_datetime = t.ctime(modification_time)

    # create a variable to hold the creation year of the current item
    # (currently works for windows only)
    sorted_dir_name = modification_datetime[len(modification_datetime)-4:]

    # create a full path for the new dir
    new_dir = os.path.join(dst_directory, sorted_dir_name)
    
    # check if the directory already exists
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

for item in src.glob('*'):

    # get the creation and modification datetime of the file
    creation_time = os.path.getctime(item)
    modification_time = os.path.getmtime(item)

    # convert the timestamps to datetime objects
    creation_datetime = t.ctime(creation_time)
    modification_datetime = t.ctime(modification_time)
