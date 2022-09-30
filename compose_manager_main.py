from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext


class ComposeManager:

    def __init__(self):

        self.win_gui = Tk()
        screen_width = self.win_gui.winfo_screenwidth() - 10
        screen_height = self.win_gui.winfo_screenheight() - 10

        self.win_gui.geometry("{}x{}+0+0".format(screen_width, screen_height))
        self.win_gui.title("Composition Manager")

        self.win_gui.mainloop()


composM = ComposeManager()