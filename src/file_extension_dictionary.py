
# This is the list of file extensions to be used in the SortingLogic class.
# SortingLogic will use these keys (e.g., 'images', 'videos', etc.) to filter items in the source directory.
# Items with extensions matching these values will be sorted, while others will be excluded.
#
# For example: If the user checks the "Images" checkbox and applies their selection,
# all files with extensions corresponding to the key 'images' (as defined below)
# will be added to the 'item_list' in the os.walk for-loop.

file_extension_dict = {
    "images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", 
        ".svg", ".webp", ".heic", ".raw", ".cr2", ".nef", ".orf", 
        ".sr2", ".arw", ".psd", ".ai", ".eps", ".indd"
    ],
    "videos": [
        ".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", 
        ".m4v", ".mpg", ".mpeg"
    ],
    "documents": [
        ".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".xls", 
        ".xlsx", ".ppt", ".pptx", ".epub", ".pages", ".key", 
        ".numbers", ".md", ".csv", ".json", ".xml", ".yaml", ".yml",
        ".tex", ".latex", ".bib", ".log"
    ],
    "audio": [
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", 
        ".aiff", ".alac"
    ]
}