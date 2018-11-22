import tkinter as tk
from tkinter import Frame, Label, StringVar, PanedWindow, Scrollbar, Canvas

SIDE_MENU_WIDTH = 250

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
        info_box = VerticalScrolledFrame(side_menu)
        info = Label(info_box.interior, bg=background, fg="white",textvariable=self.info,
                    font=("Times New Roman",14))
        info.pack()
        info.configure(justify="left")


        self.expanding_perc_1['maximum'] = 100
        self.expanding_perc_2['maximum'] = 100
        # add to side menu
        side_menu.add(state_box)
        side_menu.add(info_box)
        side_menu.sash_place(0,0,int(0.85*HEIGHT))


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            
        # create a canvas object and a vertical scrollbar for scrolling it
        background = "black"
        vscrollbar = Scrollbar(self, orient="vertical", bg=COLORS['DARK'])
        vscrollbar.pack(fill='y', side='right', expand=False)
        canvas = Canvas(self, bd=0, highlightthickness=0, bg=background,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas, background=background)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor='nw')

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
