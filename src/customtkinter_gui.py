
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
        self.geometry('300x100')

        info4 = customtkinter.CTkLabel(self, text="Welcome to Python Arranger!")
        info4.pack()
        b1 = customtkinter.CTkButton(
            self,
            text="Close",
            command=self.destroy)
        b1.pack()

        # call the function center_window
        #WindowUtils.center_window(self)
        self.resizable(False, False)
        self.transient(root)
        self.grab_set()
class MainWindow(customtkinter.CTk):
    # main window
    # creating the main window and doing some configuration
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # load icon from disk
        self.iconbitmap("C:/Users/norppa/nerdCorner/PyARR/src/titlebar_icon.ico")
        self.title("PyARR v0.1.0")
        self.geometry('600x600')
        WindowUtils.center_window(self)
        self.resizable(False, False)

        self.src_frame = source_frame(master=self,
                                      width=280,
                                      height=50)
        self.src_frame.place(x=310, y=10)

        self.dest_frame = destination_frame(master=self,
                                            width=280,
                                            height=50)
        self.dest_frame.place(x=310, y=70)

        source_dir_btn_frame = customtkinter.CTkFrame(
            self,
            width=280,
            height=50)
        source_dir_btn_frame.place(x=10, y=10)

        dest_dir_btn_frame = customtkinter.CTkFrame(
            self,
            width=280,
            height=50)
        dest_dir_btn_frame.place(x=10, y=70)

        info_frame = customtkinter.CTkFrame(
            self,
            width=580,
            height=25)
        info_frame.place(x=10, y=565)

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
        start_sorter_btn.place(x=450, y=520)

    def select_source_directory(self):
        self.src_directory = filedialog.askdirectory()
        self.src_frame.source_dir_info_label.configure(text=self.src_directory)

    def select_destination_directory(self):
        self.dst_directory = filedialog.askdirectory()
        self.dest_frame.dest_dir_info_label.configure(text=self.dst_directory)

    # call the file sorting logic with the source and destination as the parameters for it
    # use hasattr-function to check if the user has selected the src and dest folders
    def start_sorter(self):
        if hasattr(
            self,
            'src_directory') and hasattr(
                self,
                'dst_directory'):
            sort_files(
                self.src_directory,
                self.dst_directory)
        else:
            print("placeholder")
class source_frame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.source_dir_info_label = customtkinter.CTkLabel(
            self,
            text="Source folder path:",
            wraplength=260,
            width=10,
            height=30)
        self.source_dir_info_label.place(x=20, y=10)

class destination_frame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.dest_dir_info_label = customtkinter.CTkLabel(
            self,
            text="Destination folder path:",
            wraplength=260,
            width=10,
            height=30)
        self.dest_dir_info_label.place(x=20, y=10)

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