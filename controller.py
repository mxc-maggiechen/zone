from mimetypes import init
import window
import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import Image, ImageTk

window_width = 600
window_height = 750

# Driver Code

class Controller():
    def __init__(self) -> None:
        pass


def startApp():
    app = window.tkinterApp()
    app.geometry(f'{window_width}x{window_height}')
    # app = customtkinter.CTk()
    app.mainloop()
    