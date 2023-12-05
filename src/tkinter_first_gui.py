
# gui for PyARR

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from sorter import sort_files

class WelcomeWindow(Toplevel):

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.iconbitmap("C:/Users/norppa/nerdCorner/PyARR/src/titlebar_icon.ico")
        self.title("Welcome!")
        self.configure(bg="snow")
        info4 = ttk.Label(self, text="Welcome to Python Arranger!")
        info4.pack()
        b1 = ttk.Button(self, text="Close", command=self.destroy)
        b1.pack()

        # call the function center_window
        self.center_window()
        self.resizable(False, False)

    # making a function to ensure that the window opens in the middle of the screen
    def center_window(self):
        w = 300 # width of the welcome window
        h = 100 # height of the welcome window

        # get the screen width and height
        screen_x = self.winfo_screenwidth()
        screen_y= self.winfo_screenheight()

        # calculate the x and y positions for centering the window
        x = (screen_x - w) // 2
        y = (screen_y - h) // 2

        self.geometry(f'{w}x{h}+{x}+{y}')

class MainWindow(Tk):

    # main window
    # creating the main window and doing some configuration
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # load icon from disk
        self.iconbitmap("C:/Users/norppa/nerdCorner/PyARR/src/titlebar_icon.ico")
        self.title("PyARR v0.1.0")
        self.configure(bg="snow")
        self.center_window()
        self.resizable(False, False)


        # create frames
        top_frame = Frame(self, width=580, height=170, bg="PaleVioletRed1")
        top_frame.grid(row=0, column=0, padx=10, pady=5)

        middle_frame = Frame(self, width=580, height=190, bg="PaleVioletRed1")
        middle_frame.grid(row=1, column=0, padx=10, pady=5)

        bottom_frame = Frame(self, width=580, height=190, bg="PaleVioletRed1")
        bottom_frame.grid(row=2, column=0, padx=10, pady=5)

        info_frame = Frame(self, width=580, height=15, bg="purple4")
        info_frame.grid(row=3, column=0, padx=10, pady=0)

        # create frames and labels inside the first frames
        src_dir_btn = ttk.Button(self, text="Select a folder to sort...", command=self.select_source_directory)
        src_dir_btn.grid(row=0, column=0)

        dest_dir_btn2 = ttk.Button(self, text="Select a folder for the sorted items...", command=self.select_destination_directory)
        dest_dir_btn2.grid(row=1, column=0)

        start_sorter_btn = ttk.Button(self, text="Sort", command=self.start_sorter)
        start_sorter_btn.grid(row=2, column=0)
        
        


    def center_window(self):
        w = 600 # width of the welcome window
        h = 600 # height of the welcome window

        # get the screen width and height
        screen_x = self.winfo_screenwidth()
        screen_y= self.winfo_screenheight()

        # calculate the x and y positions for centering the window
        x = (screen_x - w) // 2
        y = (screen_y - h) // 2

        self.geometry(f'{w}x{h}+{x}+{y}')

    def select_source_directory(self):
        self.src_directory = filedialog.askdirectory()

    def select_destination_directory(self):
        self.dst_directory = filedialog.askdirectory()


    # call the file sorting logic with the source and destination as the parameters for it
    # use hasattr-function to check if the user has selected the src and dest folders
    def start_sorter(self):
        if hasattr(self, 'src_directory') and hasattr(self, 'dst_directory'):
            sort_files(self.src_directory, self.dst_directory)

        else:
            print("placeholder")
    


if __name__ == ("__main__"):
    main_window = MainWindow()
    welcome_window = WelcomeWindow(main_window)
    main_window.mainloop()