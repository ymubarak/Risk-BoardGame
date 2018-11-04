import tkinter as tk
from tkinter import Label, StringVar, PanedWindow

SIDE_MENU_WIDTH = 180
PHASES = ["Place Armies", "Attack!"]
COLORS = {
    'BACKGROUND': "#151315",
    'CORRECT': "#0ca972",
    'WRONG': "#ed4844",
    'DARK': "#323132"
}

class SideMenu:
    def __init__(self, WIDTH, HEIGHT):
        background = "black"
        columns = 4
        # self.embed.config(width=WIDTH-SIDE_MENU_WIDTH)
        side_menu = PanedWindow(orient="vertical", bg=COLORS['DARK'])
        side_menu.pack(fill="both", expand=1)
        side_menu.config(borderwidth=2, width=SIDE_MENU_WIDTH, height=HEIGHT, sashwidth=10)
        
        # create top state box
        state_box = tk.Frame(side_menu, width=SIDE_MENU_WIDTH*5, height=HEIGHT,
         background=background, padx=20, pady=20)
        state_box.pack(side="left", fill='both')
        
        # creating state box labels
        self.turn_phase = StringVar()
        self.turn_phase.set(PHASES[0])
        Label(state_box, bg=background, fg="green", textvariable=self.turn_phase,
         font=("Cambria",18)).grid(row=0, columnspan=columns, sticky="ew")

        self.player1_label = Label(state_box, bg=background, fg="white", text="Player1", font=("Cambria",20))
        self.player1_label.grid(row=1, columnspan=columns, sticky="nw")
        self.player1_army_label = StringVar()
        Label(state_box, bg=background, fg="white",
         textvariable=self.player1_army_label, font=("Cambria",16)).grid(row=2, columnspan=columns, sticky="nw")
        
        state_box.grid_rowconfigure(3, minsize=120)

        self.player2_label = Label(state_box, bg=background, fg="white", text="Player2", font=("Cambria",20))
        self.player2_label.grid(row=4, columnspan=columns, sticky="nw")
        self.player2_army_label = StringVar()
        self.player2_army_label.set("Armies")
        Label(state_box, bg=background, fg="white",
         textvariable=self.player2_army_label, font=("Cambria",16)).grid(row=5, columnspan=columns, sticky="w")

        # create info box
        self.side_menu_info = StringVar()
        info_box = Label(side_menu, bg=background, fg="white",textvariable=self.side_menu_info,
         font=("Times New Roman",14))
        info_box.configure(anchor="center")

        # add to side menu
        side_menu.add(state_box)
        side_menu.add(info_box)
        side_menu.sash_place(0,0,int(0.7*HEIGHT))