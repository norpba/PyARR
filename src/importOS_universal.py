import os
import shutil
from pathlib import Path

# Use os.path.expanduser() to handle ~ in the path
dst_directory = str(input("Destination directory: "))
dst_directory = os.path.expanduser(dst_directory)

# Check if the destination directory exists before creating it
if not os.path.exists(dst_directory):
    os.makedirs(dst_directory)

# Get the source directory from user input
src_directory = str(input("Source directory: "))
src = Path(src_directory).expanduser()

# Copy the contents of the source directory directly into the destination directory
for item in src.glob('*'):
    shutil.copy2(item, dst_directory)
