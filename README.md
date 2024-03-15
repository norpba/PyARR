# PyARR - Python Arranger - a simple python-based sorting tool

A simple file sorter that takes in a folder with files from the user. The script then reads the metadata of each file in the folder, from which the file creation year is used to name the folders in the output directory. Each file is then sorted into it's corresponding folder.

# Functionality

1. User chooses the source directory for the files to be sorted.
2. User then chooses an output directory for the sorted files. When the sorting button is pressed, the script sorts the files into folders, which are named by the file creation year of each file.
3. The output directory could look something like this:

       Directory:
       - C:\Users\usernamehere\Pictures\PyARR images
           - Images 2021
               - image1.png
               - image2.png
           - Images 2022
               - image3.jpeg
           - Images 2023
               - image4.png
               - image5.jpeg
               - image6.webp
    
That's about it for now. I guess we'll see how far I go with this project as I will mostly work on it on the weekend.
-norppa
