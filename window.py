import tkinter as tk
from tkinter import ttk
  
 
LARGEFONT =("Verdana", 34)
  
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
        for F in (StartPage, Login, Signup):
  
            frame = F(container, self)
  
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
  
# first window frame startpage
  
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
         
        # label of frame Layout 2
        label = ttk.Label(self, text ="Zone", font = LARGEFONT)
         
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 1, padx = 0, pady = 10)
  
        ## button to show frame 2 with text layout2
        button1 = ttk.Button(self, text ="Sign up",
        command = lambda : controller.show_frame(Signup))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 60, pady = 10)


        button2 = ttk.Button(self, text ="Login",
        command = lambda : controller.show_frame(Login))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 120, pady = 10)
  
          
  
  
# second window frame page1
class Login(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Login", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 0, pady = 10)
  
        # button to show frame 2 with text
        # layout2
     
        label1 = ttk.Label(self, text='Type in your code:')
        label1.grid(row = 1, column = 1, padx = 120, pady = 5)

        entry1 = tk.Entry (self)
        entry1.grid(row=2, column = 1, padx = 0, pady = 5)

        button2 = ttk.Button(self, text ="Submit",
                            command = lambda : controller.show_frame(StartPage))
        button2.grid(row = 3, column = 1, padx = 0, pady = 5)

        button1 = ttk.Button(self, text ="Back",
                            command = lambda : controller.show_frame(StartPage))
        button1.grid(row = 4, column = 1, padx = 120, pady = 10)

  
  
  
  
# third window frame page2
class Signup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Signup", font = LARGEFONT)
        label.grid(row = 0, column = 1, padx = 0, pady = 10)
  
        # button to show frame 2 with text
        # layout2
     
        label1 = ttk.Label(self, text='Type in your Email:')
        label1.grid(row = 1, column = 1, padx = 120, pady = 5)

        entry1 = tk.Entry (self)
        entry1.grid(row=2, column = 1, padx = 0, pady = 5)

        button2 = ttk.Button(self, text ="Submit",
                            command = lambda : controller.show_frame(StartPage))
        button2.grid(row = 3, column = 1, padx = 0, pady = 5)

        button1 = ttk.Button(self, text ="Back",
                            command = lambda : controller.show_frame(StartPage))
        button1.grid(row = 4, column = 1, padx = 120, pady = 10)
  
  
# Driver Code
app = tkinterApp()
app.mainloop()