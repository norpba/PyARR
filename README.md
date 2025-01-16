# PyARR - Python Arranger

A Python-based sorting tool for organizing files by date.

PyARR is a file sorting tool that helps organize files from a selected source directory into an output directory. Files are grouped into folders based on their creation date, structured and named by year and month.

# Features
    1. Custom Source and Output Directories:
       • Select any folder as the source for files to be sorted.
       • Define an output directory where the sorted files will be placed.
       
    2. Date-Based Organization:
       • Created folders are named based on their creation year and month.
       • Files are sorted into folders based on their creation year and month.
       
    3. Simple and Intuitive GUI:
       • Easily configure sorting preferences with a user-friendly interface.
 
 # How It Works
    1. Choose Directories:
       • Select a source directory containing the files to be sorted.
       • Specify an output directory where the sorted files will be stored.
       
    2. Sorting Process:
       • Press the Sort button to begin the process.
       • The program scans the source directory and its subfolders,
         identifies files matching the user-defined pattern, and organizes them into folders in the output directory.
       
    3  Output Structure Example:
       If the program processes image files, the output might look like this:

       Output Directory:
           - C:\Users\username\pictures\images
               - Images 2019
                   - Jun
                     - midsummer_bonfire.png
                   - Dec
                     - christmas_party.png
                     - new_years_eve.jpg
               - Images 2022
                   - Sep
                     - school_ceremony.png
               - Images 2023
                   - Jan
                     - image4.png
                     - image5.jpeg
                     - image6.webp

# Supported File Extensions

Supported File Extensions

       Images:
       .jpg, .jpeg, .png, .gif, .bmp, .tiff, .tif, .svg, .webp, .heic,
       .raw, .cr2, .nef, .orf, .sr2, .arw, .psd, .ai, .eps, .indd

       Video:
       .mp4, .mov, .avi, .mkv, .flv, .wmv, .webm, .m4v, .mpg, .mpeg

       Documents:
       .pdf, .docx, .doc, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx,
       .epub, .pages, .key, .numbers, .md, .csv, .json, .xml, .yaml,
       .yml, .tex, .latex, .bib, .log

       Audio:
       .mp3, .wav, .aac, .flac, .ogg, .wma, .m4a, .aiff, .alac

