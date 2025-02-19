
import os
import threading
import shutil
import time
import re
from pathlib import Path
from datetime import datetime
from file_extension_dictionary import file_extension_dict

import customtkinter
from CTkToolTip import *
from tkinter import filedialog, StringVar
from platform import system
from functools import partial

class MainWindow(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        icon(self)
        center_window(self, 600, 310)
        self.title("PyARR v0.5.0")
        self.resizable(False, False)
        
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.protocol("WM_DELETE_WINDOW", partial(ConfirmationWindow, self)) # capture the user closing application from toolbar and bring up ConfirmationWindow
        self.options_window = OptionsWindow(self)
        
        self.sourcepath_frame = SourcePathFrame(self)
        self.sourcepath_frame.grid(column=0, row=1, columnspan=3, rowspan=1, padx=10, pady=(0, 5), sticky="nwe")
        self.destinationpath_frame = DestinationPathFrame(self)
        self.destinationpath_frame.grid(column=0, row=2, columnspan=3, rowspan=1, padx=10, pady=(0, 5), sticky="nwe")
        
        self.progressbar_frame = ProgressBarFrame(self)
        self.progressbar_frame.grid(column=0, row=3, columnspan=2, padx=10, pady=(0, 5), sticky="nwe")
        
        self.sourcebutton_frame = SourceButtonFrame(self.sourcepath_frame, self)
        self.sourcebutton_frame.grid(column=0, row=0, padx=10, pady=(5, 5), sticky="nw")
        self.destinationbutton_frame = DestinationButtonFrame(self.destinationpath_frame, self)
        self.destinationbutton_frame.grid(column=1, row=0, padx=10, pady=(5, 5), sticky="nwe")
        
        self.sortingbutton_frame = SortButtonFrame(self,
                                                   self.sourcebutton_frame,
                                                   self.destinationbutton_frame,
                                                   self.progressbar_frame,
                                                   self.options_window
                                                   )
        self.sortingbutton_frame.grid(column=2, row=0, padx=10, pady=(5, 5), sticky="ne")
        
        self.options_frame = OptionsFrame(self, self.options_window)
        self.options_frame.grid(column=2, row=3, columnspan=1, padx=10, pady=(0, 0), sticky="ne")
        self.quitframe = QuitFrame(self)
        self.quitframe.grid(column=2, row=3, columnspan=1, padx=10, pady=(50, 0), sticky="ne")

class WelcomeWindow(customtkinter.CTkToplevel):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        icon(self)
        center_window(self, 260, 90)
        self.title("Welcome to PyARR!")
        self.resizable(False, False)
        self.transient(root)
        self.grab_set()
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        
        self.welcome_textframe = customtkinter.CTkFrame(self, corner_radius=20)
        self.welcome_textframe.grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 0), sticky="n")
        self.close_buttonframe = customtkinter.CTkFrame(self)
        self.close_buttonframe.grid(row=1, column=0, padx=10, sticky="e")
        self.about_buttonframe = customtkinter.CTkFrame(self)
        self.about_buttonframe.grid(row=1, column=1, padx=10, sticky="w")
  
        self.welcome_text = customtkinter.CTkLabel(master=self.welcome_textframe, font=('', 16), text="Welcome to Python Arranger!")
        self.welcome_text.grid(row=0, column=0, padx=7, pady=2)
        self.close_button = customtkinter.CTkButton(master=self.close_buttonframe, width=90, height=30, text="Close", command=self.destroy)
        self.close_button.grid(row=0, column=0, padx=5, pady=5)
        self.about_button = customtkinter.CTkButton(master=self.about_buttonframe, width=90, height=30, text="About", command=self.about_window)
        self.about_button.grid(row=0, column=0, padx=5, pady=5)
        
    def about_window():
        pass

class ConfirmationWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        icon(self)
        center_window(self, 350, 100)
        self.title("Confirmation")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.confirmation_label = customtkinter.CTkLabel(self, text="Are you sure you want to quit?", font=("", 14))
        self.confirmation_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.confirmation_buttonframe = customtkinter.CTkFrame(self)
        self.confirmation_buttonframe.grid(row=1, column=0, padx=10, pady=(10, 10))
        self.cancel_buttonframe = customtkinter.CTkFrame(self)
        self.cancel_buttonframe.grid(row=1, column=1, padx=10, pady=(10, 10))
        
        self.confirmation_button = customtkinter.CTkButton(master=self.confirmation_buttonframe, text="Yes", command=self.quit)
        self.confirmation_button.grid(row=0, column=0, padx=5, pady=(5, 5))
        self.cancel_button = customtkinter.CTkButton(master=self.cancel_buttonframe, text="No", command=self.destroy)
        self.cancel_button.grid(row=0, column=0, padx=5, pady=(5, 5))

class OptionsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.withdraw()
        icon(self)
        self.title("Options")
        self.resizable(False, False)
        self.grab_set()
        self.columnconfigure(3, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure((0, 1), weight=1)
        
        self.info_boxframe = customtkinter.CTkFrame(self)
        self.info_boxframe.grid(row=0, column=0, columnspan=3, padx=7, pady=(7, 0), sticky="nw")
        self.info_box = customtkinter.CTkLabel(master=self.info_boxframe, 
                                               text="Select the types of files you would like the program to sort using the checkboxes.\n\n Selecting none will result in the program sorting all file types from the source directory (except for hidden files).",
                                               wraplength=250)
        self.info_box.grid(row=0, column=0, padx=15, pady=(5, 8), sticky="we")
        
        self.checkbox_frame = OptionsCheckboxFrame(self, values=["Images", "Video", "Documents", "Audio"])
        self.checkbox_frame.grid(row=0, column=3, rowspan=2, padx=5, pady=(7, 0), sticky="ne")
        
        self.clear_buttonframe = customtkinter.CTkFrame(self)
        self.clear_buttonframe.grid(row=1, column=0, padx=7, pady=(0, 2), sticky="e")
        self.apply_buttonframe = customtkinter.CTkFrame(self)
        self.apply_buttonframe.grid(row=1, column=1, padx=19, pady=(0, 2), sticky="ew")
        self.close_buttonframe = customtkinter.CTkFrame(self)
        self.close_buttonframe.grid(row=1, column=2, padx=6, pady=(0, 2), sticky="e")
        
        self.clear_button = customtkinter.CTkButton(master=self.clear_buttonframe, width=65, text="Clear", command=self.checkbox_frame.clear_checkboxes)
        self.clear_button.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="e")
        self.apply_button = customtkinter.CTkButton(master=self.apply_buttonframe, width=65, text="Apply", command=self.checkbox_apply_callback)
        self.apply_button.grid(row=0, column=0, padx=6, pady=(5, 5), sticky="e")
        self.close_button = customtkinter.CTkButton(master=self.close_buttonframe, width=65, text="Close", command=self.close_options_window)
        self.close_button.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="e")
        
        self.selected_categories = []
        
    def checkbox_apply_callback(self):
        self.selected_categories = []
        print("before get:", self.checkbox_frame.get())
        self.checkbox_frame.get()
        
        for category in self.checkbox_frame.checked_checkboxes:
            self.selected_categories.extend(file_extension_dict.get(category, []))
        print("after for loop in apply:", self.selected_categories)
        
    def get_extension_pattern(self):
        self.pattern_str = []
        print("selected categories:", self.selected_categories)
        if self.selected_categories:
            self.pattern_str = "|".join(map(re.escape, self.selected_categories))
        else:
            self.pattern_str = '.*'
        print("pattern_str:", self.pattern_str)
        return re.compile(self.pattern_str)
    
    def close_options_window(self):
        self.withdraw()
        MainWindow.lift(self)

class OptionsCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values, checked_checkboxes=None):
        super().__init__(master)
        self.values = values
        self.checkboxes = []
        self.checked_checkboxes = checked_checkboxes if checked_checkboxes is not None else []
        
        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=1, padx=10, pady=(10, 10), sticky="e")
            self.checkboxes.append(checkbox)
            
    def get(self):
        self.checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                self.checked_checkboxes.append(checkbox.cget("text"))
                
    def clear_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.deselect()
        self.checked_checkboxes = []

class OptionsFrame(customtkinter.CTkFrame):
    def __init__(self, master, options_window, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.options_window = options_window
        
        self.options_button = customtkinter.CTkButton(self, text="Options", command=self.open_optionswindow)
        self.options_button.grid(row=0, column=0, padx=10, pady=(10, 10))
        self.tooltip = CTkToolTip(self.options_button, delay=0.5, message="Access sorting options, for example which type of files to sort.", wraplength=250)
    
    def open_optionswindow(self):
        if not hasattr(self, 'options_window') or not self.options_window.winfo_exists():
            self.options_window = OptionsWindow(self)
            self.options_window.withdraw()
            
        self.options_window.deiconify()
        self.options_window.lift()
        center_window(self.options_window, 420, 190)

class QuitFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.quitbutton = customtkinter.CTkButton(self, text="Quit", command=self.confwindow)
        self.quitbutton.grid(row=0, column=0, padx=10, pady=(10, 10))
    def confwindow(self):
        confirmation_window = ConfirmationWindow(self.master)
        center_window(confirmation_window, 350, 100)

class SourceButtonFrame(customtkinter.CTkFrame):
    def __init__(self, sourcepath_frame, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.sourcepath_frame = sourcepath_frame
        self.source_button = customtkinter.CTkButton(self, text="Select a folder to sort", command=self.SourceFolder)
        self.source_button.grid(row=0, column=0, padx=10, pady=(10, 10))
        self.tooltip = CTkToolTip(self.source_button, delay=0.5, message="Select a folder which you want to be sorted by the application.", wraplength=250)
        
    def SourceFolder(self):
        self.tooltip.hide()
        self.src_directory = filedialog.askdirectory()
        if self.src_directory:
            self.sourcepath_frame.source_stringvar.set(f"Source folder path ➙ {self.src_directory}")
            self.tooltip.show()
        else:
            self.tooltip.show()

class DestinationButtonFrame(customtkinter.CTkFrame):
    def __init__(self, destination_path_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.destination_path_frame = destination_path_frame
        self.destination_button = customtkinter.CTkButton(self, text="Select an output folder", command=self.DestinationFolder)
        self.destination_button.grid(row=0, column=1, padx=(15, 0), pady=(10, 10), sticky="we")
        self.tooltip = CTkToolTip(self.destination_button, delay=0.5, message="Select an output directory where the application will sort the files to.\nFor example this could be your 'Pictures' or 'Documents' folder.", wraplength=250)
        
    def DestinationFolder(self):
        self.tooltip.hide()
        self.dst_directory = filedialog.askdirectory()
        if self.dst_directory:
            self.destination_path_frame.dest_stringvar.set(f"Destination folder path ➙ {self.dst_directory}")
            self.tooltip.show()
        else:
            self.tooltip.show()

class SourcePathFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        def on_scroll(*args): # handle arguments being passed from scrollbar
            if args[0] == 'moveto':
                self.source_entry.xview_moveto(args[1])
                
        self.source_stringvar = StringVar(value="Source folder path ➙ ")
        self.scrollbar = customtkinter.CTkScrollbar(self, orientation="horizontal", command=on_scroll)
        self.scrollbar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nwe")
        self.scrollbar.configure(command=on_scroll)
        
        self.source_entry = customtkinter.CTkEntry(self, textvariable=self.source_stringvar, width=560, state="disabled", xscrollcommand=self.scrollbar.set)
        self.source_entry.grid(row=0, column=0, padx=10, pady=(10, 3))

class DestinationPathFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        def on_scroll(*args): # handle arguments being passed from scrollbar
            if args[0] == 'moveto':
                self.dest_entry.xview_moveto(args[1])
                
        self.dest_stringvar = StringVar(value="Destination folder path ➙ ")
        self.scrollbar = customtkinter.CTkScrollbar(self, orientation="horizontal", command=on_scroll)
        self.scrollbar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nwe")
        self.scrollbar.configure(command=on_scroll)
        
        self.dest_entry = customtkinter.CTkEntry(self, textvariable=self.dest_stringvar, width=560, state="disabled", xscrollcommand=self.scrollbar.set)
        self.dest_entry.grid(row=0, column=0, padx=10, pady=(10, 3))

class ProgressBarFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.progress_stringvar = StringVar(value="Waiting for the sorting to begin ...")
        self.progress_label = customtkinter.CTkLabel(self, textvariable=self.progress_stringvar)
        self.progress_label.grid(row=0, column=0, columnspan=7, ipady=(5), pady=(10, 10), sticky="ew")
        
        self.progress_bar = customtkinter.CTkProgressBar(self, width=370, height=20)
        self.progress_bar.grid(row=1, column=1, columnspan=5, padx=5, pady=(10, 10), sticky="we")
        self.progress_bar.set(100)
        
    def update_progress(self, progress_percentage):
        self.progress_bar.set(progress_percentage)
        self.orig_percentage = int(progress_percentage * 100)
        self.progress_stringvar.set(f"Sorting... {self.orig_percentage}% done.")

class SortButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, source_button_frame, destination_button_frame, progressbar_frame, options_window, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.source_button_frame = source_button_frame
        self.destination_button_frame = destination_button_frame
        self.progressbar_frame = progressbar_frame
        self.options_window = options_window
        
        self.sorting_button = customtkinter.CTkButton(self, text="Sort", command=self.begin_sorting_task)
        self.sorting_button.grid(row=0, column=2, padx=10, pady=(10, 10))
        self.tooltip = CTkToolTip(self.sorting_button, message="Start the sorting process.")
        
    def begin_sorting_task(self):
        try:
            self.tooltip.hide()
            if self.source_button_frame.src_directory and self.destination_button_frame.dst_directory:
                self.tooltip.show()
                self.sorting_button.configure(state='disabled')
                
                source = Path(self.source_button_frame.src_directory).expanduser()
                destination = os.path.expanduser(self.destination_button_frame.dst_directory)
                
                extension_pattern = self.options_window.get_extension_pattern()
                
                self.progressbar_thread = threading.Thread(
                    target=self.sort_files,
                    args=(source, destination, extension_pattern)
                )
                self.progressbar_thread.start()
                
        except AttributeError:
            if not self.source_button_frame.src_directory:
                error_window = ErrorWindow(self.master)
                center_window(error_window, 200, 150)
            elif not self.destination_button_frame.dst_directory:
                error_window = ErrorWindow(self.master)
                center_window(error_window, 200, 150)
                
    def sort_files(self, source, destination, extension_pattern):
        start_time = time.time()
        progress_generator = SortingLogic.sorter_logic(source, destination, extension_pattern)
        
        for progress_percentage in progress_generator:
            if progress_percentage == -1:
                self.progressbar_frame.progress_stringvar.set("No items to sort.")
                break
            self.progressbar_frame.update_progress(progress_percentage)
        
        self.sorting_button.configure(state='normal')
        self.end_time = time.time()
        if progress_percentage == 1.0:
            self.time_decimal = self.end_time - start_time
            self.progressbar_frame.progress_stringvar.set(
                f"Sorting completed. Task took {"%.2f" % self.time_decimal} seconds."
            )

class SortingLogic:
    @staticmethod
    def get_creation_date(filepath):
        try:
            stat = os.stat(filepath)
            print("st_birthtime value:", datetime.fromtimestamp(stat.st_birthtime))
            return datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            return datetime.fromtimestamp(os.path.getctime(filepath))
            
    def sorter_logic(source, destination, extension_pattern):
        total_items = 0
        item_count = 0
        percentage_check = 0.1
        item_list = []
        
        for root, dirs, files in os.walk(source):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if not file.startswith('.'):
                    if not extension_pattern or extension_pattern.search(file):
                        fullpath = os.path.join(root, file)
                        item_list.append(fullpath)
        
        if not len(item_list):
            yield -1
            return
        total_items = len(item_list)
        
        for item in item_list:
            item_count+=1
            item_date = SortingLogic.get_creation_date(item)
            
            year = item_date.strftime("%Y")
            month = item_date.strftime("%b")
            day = item_date.strftime("%d. %A")
            
            if day.startswith('0'):
                day = day[1:]
                
            print("item_count:",item_count)
            
            print(f"Year:{year} Month:{month} Day:{day}")
            print("full datetime:", item_date)
            
            year_dir = os.path.join(destination, year)
            month_dir = os.path.join(year_dir, month)
            day_dir = os.path.join(month_dir, day)
            
            os.makedirs(day_dir, exist_ok=True)
            
            final_file_path = os.path.join(day_dir, os.path.basename(item))
            shutil.copy2(item, final_file_path)
            print(final_file_path)
            progress_percentage = round(((item_count / total_items)), 2)
            if progress_percentage > percentage_check and progress_percentage <= 1.0:
                percentage_check+=0.1
                yield progress_percentage

class ErrorWindow(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        icon(self)
        self.title("An error occurred!")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        center_window(self, 200, 150)
        
def center_window(window, w, h):
    # get the screen width and height
    screen_x = window.winfo_screenwidth()
    screen_y = window.winfo_screenheight()
    # calculate the x and y positions for centering the window
    x = (screen_x - w) // 2
    y = (screen_y - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')
    
def icon(window):
    platform = system().lower()
    icon_path = ""
    
    if platform == "windows":
        icon_path = os.path.join(os.path.dirname(__file__), "icon", "icon_windows.ico")
    elif platform == "darwin":
        icon_path = os.path.join(os.path.dirname(__file__), "icon", "icon_darwin.icns")
        
    if os.path.exists(icon_path) and platform == 'windows':
        window.iconbitmap(icon_path)
    else:
        print(f"Icon file not found: {icon_path}")
    
if __name__ == ("__main__"):
    customtkinter.set_appearance_mode("system") # set UI theme
    customtkinter.set_default_color_theme("green")
    
    main_window = MainWindow()
    welcome_window = WelcomeWindow(main_window)
    src = SourceButtonFrame(main_window.sourcepath_frame, main_window)
    dst = DestinationButtonFrame(main_window.destinationpath_frame, main_window)
    sort_button_frame = SortButtonFrame(main_window, src, dst, main_window.options_window,  main_window.progressbar_frame)
    main_window.update_idletasks()
    main_window.mainloop()