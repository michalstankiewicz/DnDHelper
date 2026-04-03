import tkinter as tk
import dice
import loot
import ecounter


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DnD Helper")
        self.geometry("860x480")
