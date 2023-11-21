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
    dstdir_name = str(input("Name the folder you want the files to be copied to: "))
    os.makedirs(dst_directory)

# copy the contents of the source directory directly into the destination directory
for item in src.glob('*'):

    # get the creation and modification datetime of the file
    creation_time = os.path.getctime(item)
    modification_time = os.path.getmtime(item)

    # convert the timestamps to datetime objects
    creation_datetime = t.ctime(creation_time)
    modification_datetime = t.ctime(modification_time)

    print(creation_datetime)
    print(modification_datetime)

    shutil.copy2(item, dst_directory)