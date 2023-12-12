
# gui for PyARR

import customtkinter
from tkinter import filedialog
from sorter import sort_files

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

class WelcomeWindow(customtkinter.CTkToplevel):
    # welcome window

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.iconbitmap("C:/Users/norppa/code/PyARR/src/titlebar_icon.ico")
        self.title("Welcome!")
        self.geometry('250x150')
        self.resizable(False, False)
        self.transient(root)
        self.grab_set()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        info4 = customtkinter.CTkLabel(self,
                                       font=('', 16),
                                       text="Welcome to Python Arranger!")
        info4.grid(row=0,
                   column=0,
                   padx=10,
                   pady=(10, 0),
                   sticky="nwe")
        
        b1 = customtkinter.CTkButton(
            self,
            width=180,
            height=50,
            text="Close",
            command=self.destroy)
        b1.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="swe")
        
class MainWindow(customtkinter.CTk):
    # main window
    # creating the main window and doing some configuration

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.iconbitmap("C:/Users/norppa/code/PyARR/src/titlebar_icon.ico")
        self.title("PyARR v0.1.0")
        self.geometry('600x600')
        self.resizable(False, False)
        self.grid_columnconfigure((0, 1), weight=1)
        WindowUtils.center_window(self)
        self.sourcepath_frame = SourcePathFrame(self)
        self.sourcepath_frame.grid(columnspan=3,
                                   row=1,
                                   column=0,
                                   padx=10,
                                   pady=(10, 10),
                                   sticky="nwe")
        
        self.sourcebutton_frame = SourceButtonFrame(self.sourcepath_frame, self)
        self.sourcebutton_frame.grid(row=0,
                                     column=0,
                                     padx=10,
                                     pady=(10, 10),
                                     sticky="nw")
        
        self.destinationpath_frame = DestinationPathFrame(self)
        self.destinationpath_frame.grid(columnspan=3,
                                        row=2,
                                        column=0,
                                        padx=10,
                                        pady=(10, 10),
                                        sticky="nwe")
        
        self.destinationbutton_frame = DestinationButtonFrame(self.destinationpath_frame, self)
        self.destinationbutton_frame.grid(row=0,
                                          column=1,
                                          padx=10,
                                          pady=(10, 10),
                                          sticky="nw")
        
        self.sortingbutton_frame = SortButtonFrame(self)
        self.sortingbutton_frame.grid(row=0,
                                      column=2,
                                      padx=10,
                                      pady=(10, 10),
                                      sticky="ne")

class SourceButtonFrame(customtkinter.CTkFrame):
    def __init__(self, source_path_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.source_path_frame = source_path_frame
        self.source_button = customtkinter.CTkButton(self, text="Select a folder to sort", command=self.SourceFolder)
        self.source_button.grid(row=0, column=0, padx=10, pady=(10, 10))
        
    def SourceFolder(self):
        self.src_directory = filedialog.askdirectory()
        self.source_path_frame.source_label.configure(text=self.src_directory)
    
class DestinationButtonFrame(customtkinter.CTkFrame):
    def __init__(self, destination_path_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.destination_path_frame = destination_path_frame
        self.destination_button = customtkinter.CTkButton(self, text="Select an output folder", command=self.DestinationFolder)
        self.destination_button.grid(row=0, column=1, padx=10, pady=(10, 10))
        
    def DestinationFolder(self):
        self.dst_directory = filedialog.askdirectory()
        self.destination_path_frame.destination_label.configure(text=self.dst_directory)

class SourcePathFrame(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.source_label = customtkinter.CTkLabel(self, text="Source folder path:", wraplength=560)
        self.source_label.grid(row=0, column=0, padx=20, pady=(10, 10))

class DestinationPathFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.destination_label = customtkinter.CTkLabel(self, text="Destination folder path:", wraplength=560)
        self.destination_label.grid(row=0, column=0, padx=20, pady=(10, 10))

class SortButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.sorting_button = customtkinter.CTkButton(self, text="Sort")
        self.sorting_button.grid(row=0, column=2, padx=10, pady=(10, 10))

class Sorter:
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        
    
class WindowUtils:
    @staticmethod
    def center_window(window):
        w = 600  # width of the window
        h = 600  # height of the window

        # get the screen width and height
        screen_x = window.winfo_screenwidth()
        screen_y = window.winfo_screenheight()

        # calculate the x and y positions for centering the window
        x = (screen_x - w) // 2
        y = (screen_y - h) // 2

        #window.geometry(f'{w}x{h}+{x}+{y}')

if __name__ == ("__main__"):
    main_window = MainWindow()
    welcome_window = WelcomeWindow(main_window)
    main_window.update_idletasks()
    main_window.mainloop()