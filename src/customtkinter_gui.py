
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
        self.iconbitmap("C:/Users/norppa/nerdCorner/PyARR/src/titlebar_icon.ico")
        self.title("Welcome!")
        
        info4 = customtkinter.CTkLabel(self, text="Welcome to Python Arranger!")
        info4.pack()
        b1 = customtkinter.CTkButton(self, text="Close", command=self.destroy)
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

class MainWindow(customtkinter.CTk):
    # main window
    # creating the main window and doing some configuration

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # load icon from disk
        self.iconbitmap("C:/Users/norppa/nerdCorner/PyARR/src/titlebar_icon.ico")
        self.title("PyARR v0.1.0")
        self.center_window()
        self.resizable(False, False)

        # create frames
        top_frame = customtkinter.CTkFrame(self, width=580, height=50)
        top_frame.place(x=10, y=10)

        top_frame2 = customtkinter.CTkFrame(self, width=580, height=50)
        top_frame2.place(x=10, y=70)

        #middle_frame = customtkinter.CTkFrame(self, width=580, height=300)
        #middle_frame.place(x=10, y=100)

        #bottom_frame = customtkinter.CTkFrame(self, width=580, height=300)
        #bottom_frame.place(x=10, y=250)

        info_frame = customtkinter.CTkFrame(self, width=580, height=25)
        info_frame.place(x=10, y=565)

        # create frames and labels inside the first frames
        src_dir_btn = customtkinter.CTkButton(
            self,
            text="Select a folder to sort",
            command=self.select_source_directory)
        src_dir_btn.place(x=20, y=20)

        dest_dir_btn2 = customtkinter.CTkButton(
            self,
            text="Select a folder for the sorted items",
            command=self.select_destination_directory)
        dest_dir_btn2.place(x=20, y=80)

        start_sorter_btn = customtkinter.CTkButton(
            self,
            text="Sort",
            command=self.start_sorter)
        start_sorter_btn.place()

        self.src_dir_label = customtkinter.CTkLabel(self, text= "Source folder: ")
        self.src_dir_label.place(x=250, y=20)

        self.dst_dir_label = customtkinter.CTkLabel(self, text= "Output folder: ")
        self.dst_dir_label.place(x=250, y=80)



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
        self.src_dir_label.configure(text=self.src_directory)

    def select_destination_directory(self):
        self.dst_directory = filedialog.askdirectory()
        self.dst_dir_label.configure(text=self.dst_directory)

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