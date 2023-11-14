import os
import shutil
from pathlib import Path

# Use os.path.expanduser() to handle ~ in the path
#dst_directory = "~/myCode/PyARR/PyARR/sandbox/"
dst_directory = str(input("Give the destination directory: "))
dst_directory = os.path.expanduser(dst_directory)

# Check if the destination directory exists before creating it
if not os.path.exists(dst_directory):
    os.makedirs(dst_directory)

src_directroy = str(input("Give the source directory: "))
src = Path(src_directroy).expanduser()

# Copy the contents of the source directory directly into the destination directory
for item in src.glob('*'):
    shutil.copy2(item, dst_directory)
