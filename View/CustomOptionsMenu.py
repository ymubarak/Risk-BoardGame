import tkinter as tk
from tkinter import Label, StringVar
from tkinter.ttk import Style, OptionMenu, Button

COLORS = {
    'BACKGROUND': "#151315",
    'CORRECT': "#0ca972",
    'WRONG': "#ed4844",
    'DARK': "#323132"
}

class CustomOptionsMenu:
    def __init__(self, master, types_list):
        columns = 3
        width = 400
        height = 200
        clear_menu = lambda: options_menu.destroy()

        options_menu = self.top = tk.Frame(master, width=width, height=height,
         background=COLORS['BACKGROUND'], padx=20, pady=20)
        options_menu.place(anchor="c", relx=.5, rely=.5)
        
        player_types = types_list
        self.player1_type = StringVar()
        self.player1_type.set(player_types[0]) # set the default option
        self.player2_type = StringVar()
        self.player2_type.set(player_types[0]) # set the default option
      

        label1 = Label(options_menu, text="Player1:", font=("Calibri", 18),
         fg="white", bg=COLORS['BACKGROUND'])
        label1.grid(row=0, columnspan=columns, sticky='nw')

        popupMenu1 = OptionMenu(options_menu, self.player1_type, player_types[0], *player_types)
        popupMenu1.grid(row=1, columnspan=columns , sticky='nw')

        label2 = Label(options_menu, text="Player2:", font=("Calibri", 18),
         fg="white", bg=COLORS['BACKGROUND'])
        label2.grid(row=2, columnspan=columns, sticky='nw')

        popupMenu2 = OptionMenu(options_menu, self.player2_type, player_types[0], *player_types)
        popupMenu2.winfo_width = 15
        popupMenu2.grid(row=3, columnspan=columns , sticky='nw')

        options_menu.grid_rowconfigure(4, minsize=30)
        play_btn = Button(options_menu, text="Play", style="play_btn.TButton", command=clear_menu)
        play_btn.grid(row=5, column=2)

        s = Style()
        s.configure(
            'play_btn.TButton',
            background='green',
            foreground='green',
            font=("Cambria", 18),

        )
        s.configure("TMenubutton", font=("Cambria", 18), width="25",
         foreground="white", background=COLORS['DARK']) 
