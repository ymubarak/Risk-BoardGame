import tkinter as tk
from tkinter import Label, IntVar, Spinbox
from tkinter.ttk import Style, OptionMenu, Button

COLORS = {
    'BACKGROUND': "#151315",
    'CORRECT': "#0ca972",
    'WRONG': "#ed4844",
    'DARK': "#323132"
}

class ArmyPlacementWindow:
    def __init__(self, master, total_armies):
        columns = 3
        width = 300
        height = 150
        self.value_set = False
        clear_menu = lambda: window.destroy()
        def set_value():
            self.value_set = True
            self.num_armies = numb_spin_box.get()
            clear_menu()

        window = self.top = tk.Frame(master, width=width, height=height,
         background=COLORS['DARK'], padx=20, pady=20)
        window.place(anchor="c", relx=.5, rely=.5)
        
        label1 = Label(window, text="Place Armies in this territory:", font=("Calibri", 18),
         fg="white", bg=COLORS['DARK'])
        label1.grid(row=0, columnspan=columns, sticky='nw')

        var = IntVar()
        var.set(1) # set the default option
        numb_spin_box = Spinbox(window, from_=1, to=total_armies, textvariable=var, font=("Cambria", 18),
         width="20", fg=COLORS['DARK'], state="readonly")
        numb_spin_box.grid(row=1, columnspan=columns, sticky='nw')

        window.grid_rowconfigure(2, minsize=20)
        place_btn = Button(window, text="Place", style="custom.TButton", command=set_value)
        place_btn.grid(row=3, column=2)
        cancel_btn = Button(window, text="Cancel", style="custom2.TButton", command=clear_menu)
        cancel_btn.grid(row=3, column=1)

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
