import tkinter as tk
from tkinter import Label, StringVar, PanedWindow

SIDE_MENU_WIDTH = 180

COLORS = {
    'BACKGROUND': "#151315",
    'CORRECT': "#0ca972",
    'WRONG': "#ed4844",
    'DARK': "#323132"
}

class SideMenu:
    def __init__(self, WIDTH, HEIGHT, init_phase, player1_type, player2_type):
        background = "black"
        columns = 4
        side_menu = PanedWindow(orient="vertical", bg=COLORS['DARK'])
        side_menu.pack(fill="both", expand=1)
        side_menu.config(borderwidth=2, width=SIDE_MENU_WIDTH, height=HEIGHT, sashwidth=10)
        
        # create top state box
        state_box = tk.Frame(side_menu, width=SIDE_MENU_WIDTH*5, height=HEIGHT,
         background=background, padx=20, pady=20)
        state_box.pack(side="left", fill='both')
        
        # creating state box labels
        self.phase_name = StringVar()
        self.phase_name.set(init_phase)
        Label(state_box, bg=background, fg="green", textvariable=self.phase_name,
         font=("Cambria",18)).grid(row=0, columnspan=columns, sticky="ew")

        state_box.grid_rowconfigure(1, minsize=50)

        self.player1_label = Label(state_box, bg=background, fg="white", text="Player1", font=("Cambria",20))
        self.player1_label.grid(row=2, columnspan=columns, sticky="nw")
        label = Label(state_box, bg=background, fg="white", text=player1_type, font=("Cambria",15))
        label.grid(row=3, columnspan=columns, sticky="nw")
        
        self.player1_army_label = StringVar()
        Label(state_box, bg=background, fg="white",
         textvariable=self.player1_army_label, font=("Cambria",16)).grid(row=4, columnspan=columns, sticky="nw")
        
        label = Label(state_box, bg=background, fg="white", text="Lands Acquistion", font=("Cambria",14))
        label.grid(row=5, columnspan=columns, sticky="nw")

        self.expanding_perc_1 = tk.ttk.Progressbar(state_box, orient="horizontal", length=100)
        self.expanding_perc_1.grid(row=6, columnspan=columns, sticky="nw")

        state_box.grid_rowconfigure(7, minsize=80)

        self.player2_label = Label(state_box, bg=background, fg="white", text="Player2", font=("Cambria",20))
        self.player2_label.grid(row=8, columnspan=columns, sticky="nw")
        label = Label(state_box, bg=background, fg="white", text=player2_type, font=("Cambria",15))
        label.grid(row=9, columnspan=columns, sticky="nw")

        self.player2_army_label = StringVar()
        self.player2_army_label.set("Armies")
        Label(state_box, bg=background, fg="white",
         textvariable=self.player2_army_label, font=("Cambria",16)).grid(row=10, columnspan=columns, sticky="w")
        
        label = Label(state_box, bg=background, fg="white", text="Lands Acquistion", font=("Cambria",14))
        label.grid(row=11, columnspan=columns, sticky="nw")

        self.expanding_perc_2 = tk.ttk.Progressbar(state_box, orient="horizontal", length=100)
        self.expanding_perc_2.grid(row=12, columnspan=columns, sticky="nw")

        # create info box
        self.info = StringVar()
        info_box = Label(side_menu, bg=background, fg="white",textvariable=self.info,
         font=("Times New Roman",14))
        info_box.configure(anchor="center", justify="left")

        self.expanding_perc_1['maximum'] = 100
        self.expanding_perc_2['maximum'] = 100
        # add to side menu
        side_menu.add(state_box)
        side_menu.add(info_box)
        side_menu.sash_place(0,0,int(0.85*HEIGHT))