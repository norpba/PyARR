
# gui for PyARR
import customtkinter

from sorter import sort_files
from tkinter import filedialog, PhotoImage
from threading import Thread
from queue import Queue
from pathlib import Path

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")
class MainWindow(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icon(self)
        # calling the function center window with the parameters; self, width * height
        center_window(self, 600, 270)
        
        self.title("PyARR v0.1.0")
        self.resizable(False, False)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(3, weight=20)
        
        self.sourcepath_frame = SourcePathFrame(self)
        self.sourcepath_frame.grid(rowspan=1, columnspan=3, row=1, column=0, padx=10, pady=(0, 10), sticky="nwe")
        
        self.destinationpath_frame = DestinationPathFrame(self)
        self.destinationpath_frame.grid(rowspan=3, columnspan=3, row=2, column=0, padx=10, pady=(0, 10), sticky="nwe")
        
        self.sourcebutton_frame = SourceButtonFrame(self.sourcepath_frame, self)
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
        
        #self.frame1 = customtkinter.CTkFrame(self)
        #self.frame1.grid(row=2, column=1, columnspan=20, padx=(10, 10), pady=(5, 0), sticky="n")
        
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
        center_window(self, 490, 100)
        self.title("Sorting progress")
        self.resizable(False, False)
        self.grab_set()
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        
        self.progress_bar = customtkinter.CTkProgressBar(self, height=20)
        self.progress_bar.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 10), sticky="nwe")
        
        self.progress_bar.set(total_items)
        
        self.cancel_button = customtkinter.CTkButton(self, width=60, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=1, column=2, padx=10, pady=(10, 10), sticky="se")
        
class SourceButtonFrame(customtkinter.CTkFrame):
    def __init__(self, source_path_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.source_path_frame = source_path_frame
        self.source_button = customtkinter.CTkButton(self, text="Select a folder to sort", command=self.SourceFolder)
        self.source_button.grid(row=0, column=0, padx=10, pady=(10, 10))
        
    def SourceFolder(self):
        self.src_directory = filedialog.askdirectory()
        if self.src_directory:
            self.source_path_frame.source_label.configure(text=self.src_directory)

class DestinationButtonFrame(customtkinter.CTkFrame):
    def __init__(self, destination_path_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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
        self.source_label.grid(row=0, column=0, padx=20, pady=(10, 10))
        
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
        self.progress_queue = Queue()
        
        self.sorting_button = customtkinter.CTkButton(self, text="Sort", command=self.run_sorter)
        self.sorting_button.grid(row=0, column=2, padx=10, pady=(10, 10))

    def run_sorter(self):
        if hasattr(self.source_button_frame, 'src_directory') and hasattr(self.destination_button_frame, 'dst_directory'):
            src_directory = self.source_button_frame.src_directory
            dst_directory = self.destination_button_frame.dst_directory
            
            total_items = sum(1 for item in Path(src_directory).rglob('*') if item.is_file())
            
            print(total_items) #debug
            
            if total_items > 0:
                self.Progress_Bar_Window = ProgressBar(self, total_items)
                self.progress_queue.put(0)

                # start sorting process in a new thread
                sorter_thread = Thread(target=sort_files, args=(src_directory, dst_directory, total_items, self.progress_queue))
                sorter_thread.start()
                
                # updating the progress bar per item sorted
                while sorter_thread.is_alive():
                    progress_percentage = self.progress_queue.get(timeout=1)
                    self.Progress_Bar_Window.progress_bar.set(progress_percentage)
                    if Queue.empty:
                        pass
            else:
                print("No items") # add functionality; pop-up window to inform about src/dst directories being empty
        else:
            print("Source Directory not set.")
            
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
    sort_button_frame = SortButtonFrame(main_window, main_window.sourcebutton_frame, main_window.destinationbutton_frame)
    main_window.update_idletasks()
    main_window.mainloop()