import os
import pygame
import tkinter as tk
from tkinter import Label, StringVar, PanedWindow
from tkinter.ttk import Style, Frame, OptionMenu, Button
import networkx as nx

from Agents.Agent import Agent
import View.Colors as Colors
from GameHandler import GameHandler
from View.CustomOptionsMenu import CustomOptionsMenu
from View.SplashScreen import SplashScreen
from View.SideMenu import SideMenu
from View import Utility

#colors
BACKGROUND = (21, 19, 21) #Colors.bluey
COLORS = {
    'BACKGROUND': "#151315",
    'CORRECT': "#0ca972",
    'WRONG': "#ed4844",
    'DARK': "#323132"
}


TITLE = "Risk"
WIDTH = 1200
HEIGHT = 700
SCREEN_SIZE = (WIDTH, HEIGHT)

NODE_SIZE = 15
FPS = 14


class Game(Frame):
    def __init__(self, controller):
        super().__init__() 
        if not isinstance(controller, GameHandler):
            raise TypeError("Invalid controller, Game object must be supplied with a `GameHandler` object")
        
        self.controller = controller
        self.master.title(TITLE)
        self.master.configure(background = "black", width=WIDTH, height=HEIGHT)
        self.master.minsize(WIDTH, HEIGHT)
        # self.master.maxsize(WIDTH+SIDE_MENU_WIDTH, HEIGHT)

        self.embed = tk.Frame(self.master, width=WIDTH, height=HEIGHT) #creates embed frame for pygame window
        self.embed.grid() # Adds grid
        self.embed.pack(side='left', fill='both', expand=True) # packs window to the left
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        # create pygame
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        
    
    def _side_menu(self):
        side_menu = SideMenu(WIDTH, HEIGHT)
        self.player1_label = side_menu.player1_label
        self.player1_army_label = side_menu.player1_army_label
        self.player2_label = side_menu.player2_label
        self.player2_army_label = side_menu.player2_army_label
        self.side_menu_info = side_menu.side_menu_info

    
    def _legend(self):
        width = 300
        height = 200
        background = COLORS['BACKGROUND']
        legend = tk.Frame(self.embed, width=width, height=height,
         background = background, padx=20, pady=20)
        offsety = 0.25*height/HEIGHT
        offsetx = 0.25*width/WIDTH
        legend.place(anchor="c", relx=offsetx, rely=1-offsety)
        for i, c in enumerate(self.controller.continents()):
            color = '#%02x%02x%02x' % c.color()
            Label(legend, bg=color, text=" ", font=(None, 12)).grid(row=i, column=1)
            txt = " " + str(c.bonus())+ " bonus"
            Label(legend, bg=background, fg="white", text=txt,
             font=(None, 16)).grid(row=i, column=2)


    def _options_menu(self):
        op_menu = CustomOptionsMenu(self.master, self.controller.player_types())
        self.master.wait_window(op_menu.top)
        self.player1_type = op_menu.player1_type
        self.player2_type = op_menu.player2_type


    def _splash_screen(self):
        self.master.update()
        sp_screen = SplashScreen(self.screen, SCREEN_SIZE)


    def _build_graph(self):
        self.G = nx.Graph()
        for key in self.controller.graph().keys():
            self.G.add_node(key)
        # color nodes
        colors = []
        for c in self.controller.continents():
            colors += [c.color()] * len(c._territories)
        colors = iter(colors)
 
        positions = nx.circular_layout(self.G)
        graph_size = len(self.controller.graph())
        scale_factor = graph_size*120/4
        pos = [(p*scale_factor).astype("int") for p in positions.values()]
        min_x = min([p[0] for p in pos])
        min_y = min([p[1] for p in pos])
        x_margin = abs(min_x) + int(0.3*WIDTH)
        y_margin = abs(min_y) + int(0.3*HEIGHT)
        pos = [(p[0]+x_margin,p[1]+y_margin) for p in pos]

        # draw edges
        edge_width = 2
        for node in self.controller.graph().values():
            for nb in node.neighbors():
                v1 = pos[node.id()-1]
                v2 = pos[nb.id()-1]
                pygame.draw.line(self.screen, (255,255,255),v1, v2, edge_width)
        # draw nodes
        self.circles = []
        for i, p in enumerate(pos, start=1):
            c = pygame.draw.circle(self.screen, next(colors), (p[0],p[1]), NODE_SIZE)
            self.circles.append(c)
            Utility.draw_text(self.screen, str(i), p[0], p[1],size=NODE_SIZE+1, center=True)
        
        pygame.display.update()


    def _side_menu_labels(self, turn, players):
        color1 = "red" if turn == 0 else "white"
        color2 = "red" if turn == 1 else "white"

        self.player1_label.config(fg=color1)
        txt = "Armies: {}".format(players[0].armies)
        self.player1_army_label.set(txt)

        self.player2_label.config(fg=color2)
        txt = "Armies: {}".format(players[1].armies)
        self.player2_army_label.set(txt)
    
    
    def _init_game(self):
        # self._splash_screen()
        Utility.play_sound(0)
        self._options_menu()
        self.screen.fill(BACKGROUND)
        self._legend()
        self._side_menu()
        # build graph
        self._build_graph()
        Utility.play_sound(1)


    def run(self):
        self._init_game()
        players = self.controller.players()
        while True:
            turn, gameover = self.controller.get_game_state()
            if gameover:
                return
            
            self._side_menu_labels(turn, players)
            # check for user events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if isinstance(players[turn], Agent): # player is an AI agent
                    players[turn].play()
                else: # player is a human
                    # handle user interaction
                    pos = pygame.mouse.get_pos()
                    entered = False
                    for i, c in enumerate(self.circles, start=1):
                        if c.collidepoint(pos):
                            t = self.controller.graph()[i]
                            txt = "ID: {}\nArmies: {}\nOwner: {}".format(t.id(),
                             t.n_armies, t.owner)
                            self.side_menu_info.set(txt)
                            entered = True
                    if not entered:
                        self.side_menu_info.set("")
                            
                            

            pygame.display.update()
            self.master.update() 
