
# sorter logic modules
import os
import threading
import shutil
import time
from pathlib import Path

# UI modules
import customtkinter
from CTkToolTip import *
from tkinter import filedialog, PhotoImage, StringVar
from functools import partial

class MainWindow(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icon(self)
        center_window(self, 600, 310) # calling the function center_window with the parameters; self, width * height
        self.title("PyARR v0.1.0")
        self.resizable(False, False)
        
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        
        self.protocol("WM_DELETE_WINDOW", partial(ConfirmationWindow, self)) # capture the user closing application from toolbar and bring up ConfirmationWindow
        
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
        
        self.sortingbutton_frame = SortButtonFrame(self, self.sourcebutton_frame, self.destinationbutton_frame, self.progressbar_frame)
        self.sortingbutton_frame.grid(column=2, row=0, padx=10, pady=(5, 5), sticky="ne")
        
        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(column=2, row=3, columnspan=1, padx=10, pady=(0, 0), sticky="ne")
        
        self.quitframe = QuitFrame(self)
        self.quitframe.grid(column=2, row=3, columnspan=1, padx=10, pady=(50, 0), sticky="ne")

class WelcomeWindow(customtkinter.CTkToplevel):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        icon(self)
        center_window(self, 300, 120)
        self.title("Welcome!")
        self.resizable(False, False)
        self.transient(root)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        welcome_text = customtkinter.CTkLabel(self, font=('', 16), text="Welcome to Python Arranger!")
        welcome_text.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nwe")
        close_button = customtkinter.CTkButton(self, width=180, height=50, text="Close", command=self.destroy)
        close_button.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="swe")

class ConfirmationWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        icon(self)
        center_window(self, 350, 100)
        self.title("Confirmation")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        
        self.rowconfigure((0, 1), weight=1)
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

class OptionsFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.optionsbutton = customtkinter.CTkButton(self, text="Options")
        self.optionsbutton.grid(row=0, column=0, padx=10, pady=(10, 10))
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
        self.destination_button.grid(row=0, column=1, padx=(18, 0), pady=(10, 10), sticky="we")
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
    def __init__(self, master, source_button_frame, destination_button_frame, progressbar_frame, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.source_button_frame = source_button_frame
        self.destination_button_frame = destination_button_frame
        self.progressbar_frame = progressbar_frame
        
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
                
                self.progressbar_thread = threading.Thread(target=self.sort_files, args=(source, destination))
                self.progressbar_thread.start()
            else:
                self.tooltip.show()
        except AttributeError:
            pass # implement calling error class
            
    def sort_files(self, source, destination):
        start_time = time.time()
        progress_generator = Logic.sorter_logic(source, destination)
        for progress_percentage in progress_generator:
            print("progress_value:", progress_percentage) #debug
            self.progressbar_frame.update_progress(progress_percentage)
            if progress_percentage >= 1:
                self.sorting_button.configure(state='normal')
                self.end_time = time.time()
                self.time_decimal = self.end_time - start_time
                self.progressbar_frame.progress_stringvar.set(f"Sorting completed. Task took {"%.2f" % self.time_decimal} seconds.")
                print(f"Sorting completed in {self.time_decimal} seconds.") 
class Logic:
    @staticmethod
    def sorter_logic(source, destination):
        total_items = 0
        item_count = 0
        item_list = []
        for root, dirs, files in os.walk(source):
            for f in files:
                if not f.startswith('.'):
                    total_items+=1
                    fullpath = os.path.join(root, f)
                    item_list.append(fullpath)
                    
        for i in item_list:
            item_count+=1
            
            item_mod_date= time.ctime(os.path.getmtime(i))
            converted_date = item_mod_date[len(item_mod_date) - 4:]
            
            new_dir = os.path.join(destination, converted_date)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            destination_file_path = os.path.join(new_dir, os.path.basename(i))
            shutil.copy2(i, destination_file_path)
            
            
            progress_percentage = round(((item_count / total_items)), 2)
            if progress_percentage % 2 == 0:
                yield progress_percentage
                
def center_window(window, w, h):
    # get the screen width and height
    screen_x = window.winfo_screenwidth()
    screen_y = window.winfo_screenheight()
    # calculate the x and y positions for centering the window
    x = (screen_x - w) // 2
    y = (screen_y - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')
class ErrorWindow(customtkinter.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        icon(self) # if these do not work on other error functions, try adding it inside the function that is being called
        self.title("An error occurred!")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        
def icon(self):
    # if this does not work on macos, use 'platform.system' and make a if-statement to check whether the script runs on os or windows.
    self.wm_iconbitmap()
    self.after(199, lambda: self.wm_iconphoto(False, PhotoImage(file='titlebar_icon.png')))
if __name__ == ("__main__"):
    customtkinter.set_appearance_mode("system") # set UI theme
    customtkinter.set_default_color_theme("green")
    
    main_window = MainWindow()
    welcome_window = WelcomeWindow(main_window)
    src = SourceButtonFrame(main_window.sourcepath_frame, main_window)
    dst = DestinationButtonFrame(main_window.destinationpath_frame, main_window)
    sort_button_frame = SortButtonFrame(main_window, src, dst, main_window.progressbar_frame)
    main_window.update_idletasks()
    main_window.mainloop()
    