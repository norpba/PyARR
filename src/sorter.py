
# sorter logic for PyARR

import os
import shutil
import time
from pathlib import Path

def sort_files(src_directory, dst_directory, total_items, progress_queue):
    # use os.path.expanduser() to handle ~ in the path
    src = Path(src_directory).expanduser()
    dst_directory = os.path.expanduser(dst_directory)

    # check if the destination directory exists before creating it
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory)
    
    item_count = 0
    
    # create folders that are named after the file modification year and copy files from
    # the source directory into the newly created folders based on the file modification year
    for item in src.glob('*'):
        item_count +=1
        
        # get the creation and modification datetime of the file
        creation_time = os.path.getctime(item)
        modification_time = os.path.getmtime(item)

        # convert the timestamps to datetime objects
        creation_datetime = time.ctime(creation_time)
        #modification_datetime = time.ctime(modification_time)

        # create a variable to hold the creation year of the current item
        # seems to be working for both macOS and windows right now
        year_dir_name = creation_datetime[len(creation_datetime) - 4:]

        # create a full path for the new dir
        new_dir = os.path.join(dst_directory, year_dir_name)

        # check if the directory already exists
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        destination_file_path = os.path.join(new_dir, item.name)
        
        if item.is_dir():
            shutil.copytree(item, destination_file_path)
        else:
            shutil.copy2(item, destination_file_path)
        
        # calculate progress percentage and update the queue after every item
        if progress_queue:
            progress_percentage = (item_count / total_items) * 100
            print(progress_queue)
            progress_queue.put(progress_percentage)
    
    #sorting complete
    if progress_queue:
        progress_queue.put(100)