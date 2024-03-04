
# sorter logic modules
import os
import shutil
import time

# ui modules
import customtkinter
from tkinter import filedialog, PhotoImage, StringVar
from pathlib import Path

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
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(4, weight=20)
        
        self.sourcepath_frame = SourcePathFrame(self)
        self.sourcepath_frame.grid(rowspan=1, columnspan=3, row=1, column=0, padx=10, pady=(0, 10), sticky="nwe")
        
        self.destinationpath_frame = DestinationPathFrame(self)
        self.destinationpath_frame.grid(rowspan=3, columnspan=3, row=2, column=0, padx=10, pady=(0, 10), sticky="nwe")
        
        self.sourcebutton_frame = SourceButtonFrame(self)
        self.sourcebutton_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nw")
        
        self.destinationbutton_frame = DestinationButtonFrame(self.destinationpath_frame, self)
        self.destinationbutton_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nwe")
        
        self.sortingbutton_frame = SortButtonFrame(self, self.sourcebutton_frame, self.destinationbutton_frame)
        self.sortingbutton_frame.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="ne")
        
        self.quitframe = QuitFrame(self)
        self.quitframe.grid(row=10, column=2, padx=10, pady=(10, 10), sticky="se")
        
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

class ProgressBar(customtkinter.CTkToplevel):
    def __init__(self, master, total_items, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        icon(self)
        center_window(self, 500, 100)
        self.title("Sorting progress")
        self.resizable(False, False)
        self.grab_set()
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        
        self.total_items = total_items
        
        self.progress_bar = customtkinter.CTkProgressBar(self, height=20)
        self.progress_bar.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 10))

        self.progress_label = customtkinter.CTkLabel(self)
        self.progress_label.grid(row=1, column=1, padx=10, pady=(10, 50), sticky="we")

class SourceButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.src_directory = None
        self.source_button = customtkinter.CTkButton(self, text="Select a folder to sort", command=self.SourceFolder)
        self.source_button.grid(row=0, column=0, padx=10, pady=(10, 10))
        
    def SourceFolder(self):
        self.src_directory = filedialog.askdirectory()
        if self.src_directory:
            self.master.sortingbutton_frame.update_src_directory(self.src_directory)

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
        
class SortButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master, source_button_frame, destination_button_frame, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.source_button_frame = source_button_frame
        self.destination_button_frame = destination_button_frame
        self.src_directory = None
        self.dst_directory = None
        
        self.percent_var = StringVar()
        self.percent_var.set("0%")
        
        self.sorting_button = customtkinter.CTkButton(self, text="Sort", command=self.begin_sorting_task)
        self.sorting_button.grid(row=0, column=2, padx=10, pady=(10, 10))
        
    def update_src_directory(self, src_directory):
        self.src_destination = src_directory
    
    def begin_sorting_task(self):
        if self.src_directory and self.destination_button_frame.dst_directory:
            Logic.sorter_logic(self.src_directory, self.destination_button_frame.dst_directory)

class QuitFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.quitbutton = customtkinter.CTkButton(self, text="Quit", command=self.confwindow)
        self.quitbutton.grid(row=0, column=0, padx=10, pady=(10, 10))
        
    def confwindow(self):
        self.Confirmation_Window = ConfirmationWindow(self)

class Logic:
    @staticmethod
    def sorter_logic(src_directory, dst_directory):
        src_directory = src_directory
        dst_directory = dst_directory
        
        source = Path(src_directory).expanduser()
        destination = os.path.expanduser(dst_directory)
        
        if not os.path.exists(destination):
            os.makedirs(dst_directory)
        
        item_count = 0
        print(item_count)
        for item in source.glob('*'):
            item_count +=1    

            creation_time = os.path.getctime(item)
            modification_time = os.path.getmtime(item)
            
            creation_datetime = time.ctime(creation_time)
            modification_datetime = time.ctime(modification_time)
        
            year_dir_name = creation_datetime[len(creation_datetime) - 4:]

            new_dir = os.path.join(dst_directory, year_dir_name)

            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            
            destination_file_path = os.path.join(new_dir, item.name)
            
            if item.is_dir():
                shutil.copytree(item, destination_file_path)
            else:
                shutil.copy2(item, destination_file_path)
            
            #progress_percentage = (item_count / total_items) * 100
            
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
    
    src = SourceButtonFrame(main_window)
    dst = DestinationButtonFrame(main_window.destinationpath_frame, main_window)
    
    sort_button_frame = SortButtonFrame(main_window, src, dst)
    
    main_window.update_idletasks()
    main_window.mainloop()