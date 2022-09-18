import tkinter as tk
from tkinter import *
from tkinter.tix import IMAGETEXT
from turtle import bgcolor
import customtkinter
import zone;
from PIL import Image, ImageTk
import tkinter as tk
import pyglet,tkinter
pyglet.font.add_file('futura_medium_bt.ttf')


# main()

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
window_width = 600
window_height = 750
phone = +11231231234
# 600, 750
 
LARGEFONT = ("futura_medium_bt", 39)
MIDFONT = ("futura_medium_bt", 18)

DARK_BLUE = '#003049'
DARK_PURPLE = '#5F0F40'
BG_COLOR = '#EDE6C0'
  
class tkinterApp(tk.Tk):
    
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        bg = PhotoImage(file = "bg1.png")

        for F in (StartPage, Login, Signup, Menu, Contact, Setup, Shift):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            # frame.config(container, image=bg)

  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
# Start page
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        img = ImageTk.PhotoImage(Image.open(
            'bg1.png').resize((600, 750), Image.ANTIALIAS))


        lbl = tk.Label(self, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        # Place label in center of parent.
        lbl.place(relx=0.5, rely=0.5, anchor='center')

        path = "logored.png"
        img = ImageTk.PhotoImage(Image.open('logored.png').resize((420, 120), Image.ANTIALIAS))
        panel = Label(self, image=img)
        panel.photo = img
        panel.place(width=472, height=293, x=window_width/2, y=270, anchor="center")

        # title_img = ImageTk.PhotoImage(Image.open(
        #     'logored.png').resize((472, 293), Image.ANTIALIAS))
        # title_lbl = tk.Label(self, image = title_img)
        # title_lbl.place()
        # # label of frame Layout 2
        # title_lbl.place(anchor="center", x=window_width/2, y=270)
        # # putting the grid in its place by using
        # # grid
        # # label.grid(row = 0, column = 1, padx = 0, pady = 10)

        button1 = customtkinter.CTkButton(self, text ="Log in", text_font = MIDFONT,

        command = lambda : controller.show_frame(Login))
     
        # putting the button in its place by
        # using grid
        # button1.grid(row = 1, column = 1, padx = 120, pady = (100, 10))
        button1.place(x=window_width/2, y=460, anchor="center")

        ## button to show frame 2 with text layout2
        button2 = customtkinter.CTkButton(self, text ="Sign up", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
        command = lambda : controller.show_frame(Signup))
     
        # putting the button in its place by
        # using grid
        button2.place(x=window_width/2, y=510, anchor="center")
          
  
  
# Login page
class Login(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)

        img = ImageTk.PhotoImage(Image.open('bg1.png').resize((600, 750), Image.ANTIALIAS))
        lbl = tk.Label(self, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.

        label = customtkinter.CTkLabel(self, text ="Log in", text_font = LARGEFONT, bg_color = BG_COLOR)
        label.grid(row = 0, column = 1, padx = 0, pady = 10)
        label.place(x=window_width/2, y=200, anchor="center")

  
        # button to show frame 2 with text
        # layout2
     
        label1 = customtkinter.CTkLabel(self, text='Type in your code:', text_font = MIDFONT, anchor='center', bg_color = BG_COLOR)
        label1.place(x=window_width/2-80, anchor="center", y=335)

        entry1 = customtkinter.CTkEntry (self, text_font = MIDFONT)
        entry1.place(x=window_width/2+30, y=320)

        button2 = customtkinter.CTkButton(self, text ="Submit", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : controller.show_frame(Menu))
        button2.place(x=window_width/2, y=450, anchor = "center")

        button1 = customtkinter.CTkButton(self, text ="Back", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : controller.show_frame(StartPage))
        button1.place(x=window_width/2, y=500, anchor = "center")

  
  
  
  
# Signup page
class Signup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = ImageTk.PhotoImage(Image.open('bg1.png').resize((600, 750), Image.ANTIALIAS))
        lbl = tk.Label(self, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.

        label = customtkinter.CTkLabel(self, text ="Sign up", text_font = LARGEFONT, bg_color = BG_COLOR)
        label.place(x=window_width/2, y=200, anchor="center")
  
        # button to show frame 2 with text
        # layout2
     
        label1 = customtkinter.CTkLabel(self, text='Type in your phone number:', text_font=MIDFONT, bg_color = BG_COLOR)
        label1.place(x=window_width/2, y=300, anchor="center")

        entry1 = customtkinter.CTkEntry (self, text_font=MIDFONT, width=500)
        entry1.place(x=window_width/2, y=340, anchor="center")

        button2 = customtkinter.CTkButton(self, text ="Submit", text_font=MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : controller.show_frame(Setup))
        button2.place(x=window_width/2, y=450, anchor="center")

        button1 = customtkinter.CTkButton(self, text ="Back", text_font=MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : controller.show_frame(StartPage))
        button1.place(x=window_width/2, y=500, anchor="center")

# Menu page
class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = ImageTk.PhotoImage(Image.open('bg1.png').resize((600, 750), Image.ANTIALIAS))
        lbl = tk.Label(self, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.

        label = customtkinter.CTkLabel(self, text ="Menu", text_font = LARGEFONT, bg_color = BG_COLOR)
        label.place(x=window_width/2, y=200, anchor="center")

        button1 = customtkinter.CTkButton(self, text ="Backup Contact", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : controller.show_frame(Contact))
        button1.place(x=window_width/2, y=350, anchor="center")

        button2 = customtkinter.CTkButton(self, text ="Start shift", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : controller.show_frame(Shift))
        button2.place(x=window_width/2, y=430, anchor="center")

        button3 = customtkinter.CTkButton(self, text ="Update baseline", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : controller.show_frame(Setup))
        button3.place(x=window_width/2, y=510, anchor="center")

def submitphone(self, parent, controller, value):
    phone=value
    controller.show_frame(Menu)
    

# Contact page
class Contact(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = ImageTk.PhotoImage(Image.open('bg1.png').resize((600, 750), Image.ANTIALIAS))
        lbl = tk.Label(self, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.


        label = customtkinter.CTkLabel(self, text ="Contact Method", text_font = LARGEFONT, bg_color = BG_COLOR)
        label.place(x=window_width/2, y=200, anchor = "center")

        label1 = customtkinter.CTkLabel(self, text='Email:', text_font = MIDFONT, bg_color = BG_COLOR)
        label1.place(x=window_width/2-150, y=330, anchor = "center")

        entry1 = customtkinter.CTkEntry (self, text_font = MIDFONT, width = 300)
        entry1.place(x=window_width/2+40, y=330, anchor = "center")

        label2 = customtkinter.CTkLabel(self, text='Number:', text_font = MIDFONT, bg_color = BG_COLOR)
        phone = entry1.get()
        label2.place(x=window_width/2-165, y=400, anchor = "center")

        entry2 = customtkinter.CTkEntry (self, text_font = MIDFONT, width=300)
        entry2.place(x=window_width/2+40, y=400, anchor = "center")

        button2 = customtkinter.CTkButton(self, text ="Submit", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : submitphone(self, parent, controller, entry2.get()))
        button2.place(x=window_width/2, y=500, anchor = "center")

# Setup
class Setup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = ImageTk.PhotoImage(Image.open('bg1.png').resize((600, 750), Image.ANTIALIAS))
        lbl = tk.Label(self, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.

        label = customtkinter.CTkLabel(self, text ="Please click the button below.", text_font = ("Verdana", 27), bg_color = BG_COLOR)
        label.place(x=window_width/2, y=270, anchor = 'center')

        button = customtkinter.CTkButton(self, text ="Continue to Eye Scanning",  text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR, bg_color = BG_COLOR,
                            command = lambda : zone.main(phone))
        button.place(x=window_width/2, y=350, anchor = 'center')

        button = customtkinter.CTkButton(self, text ="Quit",  text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR, bg_color = BG_COLOR,
                            command = lambda : controller.show_frame(Menu))
        button.place(x=window_width/2, y=400, anchor = 'center')

# Shift
class Shift(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = ImageTk.PhotoImage(Image.open('bg1.png').resize((600, 750), Image.ANTIALIAS))
        lbl = tk.Label(self, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function.
        lbl.place(relx=0.5, rely=0.5, anchor='center')  # Place label in center of parent.


        label = customtkinter.CTkLabel(self, text ="Plug in your MindLink and", text_font = ("Verdana", 27), bg_color = BG_COLOR)
        label.place(x=window_width/2, y=250, anchor = 'center')

        label = customtkinter.CTkLabel(self, text ="ensure AdHawk Backend", text_font = ("Verdana", 27), bg_color = BG_COLOR)
        label.place(x=window_width/2, y=300, anchor = 'center')

        label = customtkinter.CTkLabel(self, text ="is running.", text_font = ("Verdana", 27), bg_color = BG_COLOR)
        label.place(x=window_width/2, y=350, anchor = 'center')

        button = customtkinter.CTkButton(self, text ="Begin", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : zone.main(phone))
        button.place(x=window_width/2, y=430, anchor = 'center')

        button = customtkinter.CTkButton(self, text ="Quit", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
                            command = lambda : controller.show_frame(Menu))
        button.place(x=window_width/2, y=490, anchor = 'center')

        # button = customtkinter.CTkButton(self, text ="show", text_font = MIDFONT, fg_color=DARK_BLUE, text_color=BG_COLOR,
        #                     command = lambda : print(phone))
        # button.place(x=window_width/2, y=580, anchor = 'center')
  
# Driver Code
app = tkinterApp()
app.geometry(f'{window_width}x{window_height}')
app.title= 'Vision'
app.wm_attributes('-transparentcolor','black')
# app = customtkinter.CTk()
app.mainloop()