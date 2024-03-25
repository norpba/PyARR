
# sorter logic modules
import os
import threading
import shutil
import time
from pathlib import Path

# ui modules
import customtkinter
from tkinter import filedialog, PhotoImage
from functools import partial

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

class MainWindow(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icon(self)
        # calling the function center window with the parameters; self, width * height
        center_window(self, 600, 370)
        
        self.title("PyARR v0.1.0")
        self.resizable(False, False)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=10)
        self.grid_rowconfigure(4, weight=20)
        
        self.protocol("WM_DELETE_WINDOW", partial(ConfirmationWindow, self))
        
        self.sourcepath_frame = SourcePathFrame(self)
        self.sourcepath_frame.grid(rowspan=2, columnspan=3, row=1, column=0, padx=10, pady=(0, 10), sticky="nwe")
        
        self.destinationpath_frame = DestinationPathFrame(self)
        self.destinationpath_frame.grid(rowspan=2, columnspan=3, row=2, column=0, padx=10, pady=(20, 10), sticky="nwe")
        
        self.progressbar_frame = ProgressBarFrame(self)
        self.progressbar_frame.grid(rowspan=1, columnspan=3, row=3, column=0, padx=10, pady=(35, 0), sticky="we")
        
        self.sourcebutton_frame = SourceButtonFrame(self.sourcepath_frame, self)
        self.sourcebutton_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nw")
        
        self.destinationbutton_frame = DestinationButtonFrame(self.destinationpath_frame, self)
        self.destinationbutton_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nwe")
        
        self.sortingbutton_frame = SortButtonFrame(self, self.sourcebutton_frame, self.destinationbutton_frame, self.progressbar_frame)
        self.sortingbutton_frame.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="ne")
        
        self.quitframe = QuitFrame(self)
        self.quitframe.grid(row=10, column=2, padx=10, pady=(0, 10), sticky="se")

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
        
        info4 = customtkinter.CTkLabel(self, font=('', 16), text="Welcome to Python Arranger!")
        info4.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nwe")
        b1 = customtkinter.CTkButton(self, width=180, height=50, text="Close", command=self.destroy)
        b1.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="swe")

class ConfirmationWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
        icon(self)
        center_window(self, 350, 100)
        self.title("Confirmation")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        
        self.confirmation_label = customtkinter.CTkLabel(self, text="Are you sure you want to quit?", font=("", 14))
        self.confirmation_label.grid(row=2, column=1, columnspan=20, padx=(10, 10))
        
        self.confirmation_button = customtkinter.CTkButton(self, width=70, height=25, text="Yes", command=self.quit)
        self.confirmation_button.grid(row=5, column=6, pady=(10, 15), sticky="se")
        
        self.cancel_button = customtkinter.CTkButton(self, width=70, height=25, text="No", command=self.destroy)
        self.cancel_button.grid(row=5, column=7, padx=20, pady=(10, 15), sticky="se")

class SourceButtonFrame(customtkinter.CTkFrame):
    def __init__(self, sourcepath_frame, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.sourcepath_frame = sourcepath_frame
        self.src_directory = None
        self.source_button = customtkinter.CTkButton(self, text="Select a folder to sort", command=self.SourceFolder)
        self.source_button.grid(row=0, column=0, padx=10, pady=(10, 10))
        
    def SourceFolder(self):
        self.src_directory = filedialog.askdirectory()
        if self.src_directory:
            self.master.sortingbutton_frame.update_src_directory(self.src_directory)
            self.sourcepath_frame.source_label.configure(text=self.src_directory)

class DestinationButtonFrame(customtkinter.CTkFrame):
    def __init__(self, destination_path_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.dst_directory = None
        self.destination_path_frame = destination_path_frame
        
        self.destination_button = customtkinter.CTkButton(self, text="Select an output folder", command=self.DestinationFolder)
        self.destination_button.grid(row=0, column=1, padx=(15, 0), pady=(10, 10), sticky="nwe")
        
    def DestinationFolder(self):
        self.dst_directory = filedialog.askdirectory()
        if self.dst_directory:
            self.destination_path_frame.destination_label.configure(text=self.dst_directory)

class SourcePathFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.source_label = customtkinter.CTkLabel(self, text="Source folder path:", wraplength=560)
        self.source_label.grid(row=1, column=0, padx=20, pady=(10, 10))

class DestinationPathFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.destination_label = customtkinter.CTkLabel(self, text="Destination folder path:", wraplength=560)
        self.destination_label.grid(row=0, column=0, padx=20, pady=(10, 10))

class ProgressBarFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.progress_label = customtkinter.CTkLabel(self)
        self.progress_label.grid(row=0, column=1, padx=10, pady=(10, 10))
        
        self.progress_bar = customtkinter.CTkProgressBar(self, width=560, height=20)
        self.progress_bar.grid(row=1, column=1, columnspan=5, padx=10, pady=(10, 10))
        
        self.progress_bar.set(100)
        
    def update_progress(self, progress_percentage):
        self.progress_bar.set(progress_percentage)

class SortButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, source_button_frame, destination_button_frame, progressbar_frame, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.source_button_frame = source_button_frame
        self.destination_button_frame = destination_button_frame
        self.progressbar_frame = progressbar_frame
        self.progressbar_thread = None
        
        self.sorting_button = customtkinter.CTkButton(self, text="Sort", command=self.begin_sorting_task)
        self.sorting_button.grid(row=0, column=2, padx=10, pady=(10, 10))
        
    def update_src_directory(self, src_directory):
        self.src_directory = src_directory
    
    def begin_sorting_task(self):
        if self.source_button_frame.src_directory and self.destination_button_frame.dst_directory:
            self.sorting_button.configure(state='disabled')
            source = Path(self.source_button_frame.src_directory).expanduser()
            destination = os.path.expanduser(self.destination_button_frame.dst_directory)
            self.progressbar_thread = threading.Thread(target=self.sort_files, args=(source, destination))
            self.progressbar_thread.start()
            
    def sort_files(self, source, destination):
        progress_generator = Logic.sorter_logic(source, destination)
        for progress_percentage in progress_generator:
            print("progress_value:", progress_percentage) #debug
            if progress_percentage >= 1:
                self.sorting_button.configure(state='normal')
            self.progressbar_frame.update_progress(progress_percentage)
            
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
            print(i)
            item_count+=1 # <----- continue 
            
            item_mod_date= time.ctime(os.path.getmtime(i))
            converted_date = item_mod_date[len(item_mod_date) - 4:]
            
            new_dir = os.path.join(destination, converted_date)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
                        
            destination_file_path = os.path.join(new_dir, os.path.basename(i))
            shutil.copy2(i, destination_file_path)

            progress_percentage = ((item_count / total_items) * 100) / 100.0
            yield progress_percentage
            
class QuitFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.quitbutton = customtkinter.CTkButton(self, text="Quit", command=self.confwindow)
        self.quitbutton.grid(row=0, column=0, padx=10, pady=(10, 10))
        
    def confwindow(self):
        self.Confirmation_Window = ConfirmationWindow(self)
        
def icon(self):
    # if this does not work on macos, use 'platform.system' and make a if-statement to check whether the script runs on os or windows.
    self.wm_iconbitmap()
    self.after(199, lambda: self.wm_iconphoto(False, PhotoImage(file='titlebar_icon.png')))
           
def center_window(window, w, h):
    # get the screen width and height
    screen_x = window.winfo_screenwidth()
    screen_y = window.winfo_screenheight()
    # calculate the x and y positions for centering the window
    x = (screen_x - w) // 2
    y = (screen_y - h) // 2
    window.geometry(f'{w}x{h}+{x}+{y}')
     
if __name__ == ("__main__"):
    main_window = MainWindow()
    welcome_window = WelcomeWindow(main_window)
    
    src = SourceButtonFrame(main_window.sourcepath_frame, main_window)
    dst = DestinationButtonFrame(main_window.destinationpath_frame, main_window)
    
    sort_button_frame = SortButtonFrame(main_window, src, dst, main_window.progressbar_frame)
    
    main_window.update_idletasks()
    main_window.mainloop()