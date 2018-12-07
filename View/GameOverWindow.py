import tkinter as tk
from tkinter import Label, StringVar
from tkinter.ttk import Style, OptionMenu, Button
from View import Utility

COLORS = {
    'BACKGROUND': "black",
    'GREENY': "#0ca972",
    'REDY': "#ed4844",
    'DARK': "#323132"
}

class GameOverWindow:
    def __init__(self, master, header, summary):
        Utility.play_sound(2)
        columns = 3
        width = 600
        height = 800
        
        self.play_again = False
        quit = lambda: window.destroy()
        def play_again():
            self.play_again = True
            quit()

        window = self.top = tk.Frame(master, width=width, height=height,
         background=COLORS['BACKGROUND'], padx=20, pady=20)
        window.place(anchor="c", relx=.5, rely=.5)
              

        label = Label(window, text="Game Over", font=("Wide Latin", 26),
         fg="white", bg=COLORS['BACKGROUND'])
        label.grid(row=0, columnspan=columns, sticky='we')

        label = Label(window, text=header, font=("Wide Latin", 20),
         fg=COLORS['GREENY'], bg=COLORS['BACKGROUND'])
        label.grid(row=1, columnspan=columns, sticky='we')

        window.grid_rowconfigure(2, minsize=10)

        label = Label(window, text=summary , font=("Cambria", 16),
         fg="white", bg=COLORS['BACKGROUND'])
        label.grid(row=3, columnspan=columns, sticky='we')
        
        window.grid_rowconfigure(4, minsize=10)
        
        place_btn = Button(window, text="View History", style="custom.TButton", command=play_again)
        place_btn.grid(row=5, column=2)
        
        cancel_btn = Button(window, text="Exit", style="custom2.TButton", command=quit)
        cancel_btn.grid(row=5, column=1)

        s = Style()
        s.configure(
            'custom.TButton',
            background='green',
            foreground='green',
            font=("Cambria", 18),

        )
        s.configure(
            'custom2.TButton',
            background='red',
            foreground='red',
            font=("Cambria", 18),

        )