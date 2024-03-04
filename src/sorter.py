
# sorter logic for PyARR

import os
import shutil
import time
from pathlib import Path

def sort_files(src, dst, total_items, progress_queue, percent_var):
    
    # use os.path.expanduser() to handle ~ in the path
    src = Path(src).expanduser()
    dst_directory = os.path.expanduser(dst)

    # check if the destination directory exists before creating it
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory)
    
    item_count = 0
    
    # create folders that are named after the file modification year and copy files from
    # the source directory into the newly created folders based on the file modification year
    for item in src.glob('*'):
        item_count +=1
        
        # get the creation and modification datetime of the file
        # currently using creation datetime to sort the files
        creation_time = os.path.getctime(item)
        modification_time = os.path.getmtime(item)

        # convert the timestamps to datetime objects
        creation_datetime = time.ctime(creation_time)
        
        # not being used right now
        # modification_datetime = time.ctime(modification_time)

        # create a variable to hold the creation year of the current item
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
        
        time.sleep(5)
        
        progress_percentage = (item_count / total_items) * 100
        percent_var.set(f"{progress_percentage:.2f}%")
        progress_queue.put(progress_percentage)
    
    progress_queue.put("DONE")
    percent_var.set("100.0%")
    progress_queue.put(100.0)