import os
import pygame
import tkinter as tk
from tkinter import Label, Canvas, PhotoImage
from tkinter.ttk import Frame
import networkx as nx
from PIL import ImageTk, Image

from Agents.Agent import Agent
import View.Colors as Colors
from GameHandler import GameHandler
from View.CustomOptionsMenu import CustomOptionsMenu
from View.GameOverWindow import GameOverWindow
from View.SplashScreen import SplashScreen
from View.SideMenu import SideMenu
from View.ArmyPlacementWindow import ArmyPlacementWindow
from View import Utility

#colors
BACKGROUND = (21, 19, 21) #Colors.bluey
COLORS = {
    'BACKGROUND': "#151315",
    'GREENY': "#0ca972",
    'REDY': "#ed4844",
    'LIGHTREDY': '#e59d9c',
    'DARK': "#323132"
}


TITLE = "Risk"
WIDTH = 1200
HEIGHT = 700
SCREEN_SIZE = (WIDTH, HEIGHT)
EDGE_WIDTH = 2
NODE_SIZE = 200
FPS = 14

# paths
STANDING_SOLJ = "media/images/standing{}.png"
FIGHTING_SOLJ = "media/images/fighting{}.png"

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
        self.side_menu = SideMenu(WIDTH, HEIGHT, self.controller.game_phase()[1])

    
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
            color = Colors.to_hex(c.color())
            Label(legend, bg=color, text=" ", font=(None, 12)).grid(row=i, column=1)
            txt = " " + str(c.bonus())+ " bonus"
            Label(legend, bg=background, fg="white", text=txt,
             font=(None, 16)).grid(row=i, column=2)


    def _options_menu(self):
        op_menu = CustomOptionsMenu(self.master, self.controller.player_types())
        self.master.wait_window(op_menu.top)
        self.controller.create_players(op_menu.player1_type.get(),
         op_menu.player2_type.get())


    def _splash_screen(self):
        self.master.update()
        sp_screen = SplashScreen(self.screen, SCREEN_SIZE)


    def _army_placement_window(self, armies):
        placment_window = ArmyPlacementWindow(self.master, armies)
        self.master.wait_window(placment_window.top)
        if placment_window.value_set:
            return int(placment_window.num_armies)
    
    def _skip_button(self):
        width = 80
        height = 40
        x1 = WIDTH/2 - width/2
        y1 = -height
        x2 = x1 + width
        y2 = 0
        top_padding = 20
        left_padding = 39

        self.skip_button_rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLORS['REDY'])
        self.skip_button_txt = self.canvas.create_text(x1+left_padding, y1+top_padding,
         text="Skip", fill="white", font=(None, 14))
        WAIT_TIME = 5
        def sign(n):
            if n > 0: return 1
            elif n < 0: return -1
            return 0
        
        def _moveloop(object_id, tomovex, tomovey):
            if not tomovex and not tomovey:
                return  # Break the loop
            
            self.canvas.move(object_id, sign(tomovex), sign(tomovey))
            newx = (abs(tomovex) - 1) * sign(tomovex)
            newy = (abs(tomovey) - 1) * sign(tomovey)

            self.master.after(WAIT_TIME, lambda: _moveloop(object_id, newx, newy))
        self.canvas.animate = _moveloop
        # self.skip_button_txt = Utility.draw_text(self.screen, "Skip", WIDTH/2+width/2 ,top_padding, 18)

    def _show_skip_button(self):
        height = 40
        coords = self.canvas.coords(self.skip_button_rect)
        if coords[1] == -height:
            self.canvas.animate(self.skip_button_rect, 0, height)
            self.canvas.animate(self.skip_button_txt, 0, height)

    def _hide_skip_button(self):
        height = 40
        coords = self.canvas.coords(self.skip_button_rect)
        if coords[1] == 0:
            self.canvas.animate(self.skip_button_rect, 0, -height)
            self.canvas.animate(self.skip_button_txt, 0, -height)

    def _side_menu_labels(self, turn, players):
        color1 = "red" if turn == 0 else "white"
        color2 = "red" if turn == 1 else "white"

        self.side_menu.player1_label.config(fg=color1)
        txt = "Armies: {}".format(players[0].armies)
        self.side_menu.player1_army_label.set(txt)

        self.side_menu.player2_label.config(fg=color2)
        txt = "Armies: {}".format(players[1].armies)
        self.side_menu.player2_army_label.set(txt)
        self.side_menu.phase_name.set(self.controller.game_phase()[1])
        
        pls = self.controller.players()
        self.side_menu.expanding_perc_1['value'] = 100*len(pls[0]._territories)/self.graph_size
        self.side_menu.expanding_perc_1.update()
        self.side_menu.expanding_perc_2['value'] = 100*len(pls[1]._territories)/self.graph_size
        self.side_menu.expanding_perc_2.update()
    
    
    def _build_graph(self):
        self.G = nx.Graph()
        for key in self.controller.graph().keys():
            self.G.add_node(key)
        # color nodes
        colors = []
        for c in self.controller.continents():
            colors += [Colors.to_hex(c.color())] * len(c._territories)
        colors = iter(colors)
 
        positions = nx.circular_layout(self.G)
        self.graph_size = len(self.controller.graph())
        scale_factor = 440/self.graph_size
        pos = [(p*scale_factor).astype("int") for p in positions.values()]
        min_x = min([p[0] for p in pos])
        min_y = min([p[1] for p in pos])
        x_margin = abs(min_x) + int(0.3*WIDTH)
        y_margin = abs(min_y) + int(0.3*HEIGHT)
        pos = [(p[0]+x_margin,p[1]+y_margin) for p in pos]

        # draw edges
        explored = set()
        self.edges = []
        for node in self.controller.graph().values():
            for nb in node.neighbors():
                if (node, nb) not in explored:
                    explored.add((node, nb))
                    explored.add((nb, node))
                    v1 = pos[node.id()-1]
                    v2 = pos[nb.id()-1]
                    edge = self.canvas.create_line(v1[0], v1[1], v2[0], v2[1],
                     width=EDGE_WIDTH, fill="white", smooth=True)
                    self.edges.append((node, nb, edge))
                
        # draw nodes
        self.circles = []
        self.circles_positions = {}
        global NODE_SIZE
        NODE_SIZE = NODE_SIZE//self.graph_size
        for i, p in enumerate(pos, start=1):
            object_id = self.canvas.create_circle(p[0], p[1], NODE_SIZE, fill=next(colors), width=2)
            self.circles.append(object_id)
            self.circles_positions[object_id] = (p[0], p[1])
            # Utility.draw_text(self.screen, str(i), p[0], p[1],size=NODE_SIZE+1, center=True)
        
    
    def _highlight_attackables(self, territory):
        turn, _ = self.controller.get_game_state()
        players = self.controller.players()
        edges = []
        if players[turn].has_territory(territory):
            atks = territory.attackables()
            for a in atks:
                for tpl in self.edges:
                    if tpl.count(territory)==1 and tpl.count(a)==1:
                        edges.append(tpl[-1])
                        continue
        for e in edges:
            self.canvas.itemconfigure(e, fill=COLORS['REDY'], width=4)


    def _motion(self, pos):
        if self.game_over:
            return
        entered = False
        object_ids = self.canvas.find_overlapping(pos.x,
            pos.y, pos.x+1, pos.y+1)
        
        if object_ids:
            if object_ids[0] == self.skip_button_rect:
                self.canvas.itemconfigure(object_ids[0], 
                    fill=COLORS['LIGHTREDY'])
                return                

            if object_ids[0] not in self.circles:
                return
            self.canvas.last_object = object_ids[0]
            self.canvas.itemconfigure(object_ids[0],
                outline="white", width=3)
            
            index = self.circles.index(object_ids[0])
            territory = self.controller.graph()[index+1]
            self._highlight_attackables(territory)

            owner = None
            if territory.owner != None:
                ps = self.controller.players()
                p_num = 1 if territory.owner==ps[0] else 2
                owner = "Player "+str(p_num)
            txt = "Owner: {}\nArmies: {}\nID: {}".format(owner,
                territory.n_armies, territory.id())
            self.side_menu.info.set(txt)
            #self._hide_skip_button()
            entered = True
          
        if not entered:
            self.side_menu.info.set("")
            self.canvas.itemconfigure(self.skip_button_rect, 
                    fill=COLORS['REDY'])
            if not self.attacker_choosed:
                for tpl in self.edges:
                    self.canvas.itemconfigure(tpl[-1], fill="white", width=EDGE_WIDTH)
            if self.canvas.last_object in self.circles:
                self.canvas.itemconfigure(self.canvas.last_object,
                    outline="black", width=2)
    
    def _user_play(self, pos):
        if self.game_over:
            return
        if self.is_agent_player:
            return
        object_ids = self.canvas.find_overlapping(pos.x,
            pos.y, pos.x+1, pos.y+1)
        
        if not object_ids:
            return
        # skip button clicked
        if object_ids[0] == self.skip_button_rect:
            self._hide_skip_button()
            self.controller.change_phase()
            self.controller.switch_turn()
            self.is_new_turn = True
            self.attacker_choosed = None
            return
        
        if object_ids[0] not in self.circles:
            return
        index = self.circles.index(object_ids[0])
        territory = self.controller.graph()[index+1]

        turn, _ = self.controller.get_game_state()
        players = self.controller.players()
        if self.controller.game_phase()[0] == 0: # place armies
            other_player = 0 if turn==1 else 1
            if players[other_player].has_territory(territory):
                return
            
            placed_armies = self._army_placement_window(players[turn].armies)
            if placed_armies is None:
                return
            territory.n_armies+= placed_armies
            players[turn].armies -= placed_armies
            if not players[turn].has_territory(territory):
                players[turn].add_territory(territory)
            
            img_file = Image.open(STANDING_SOLJ.format(turn+1))
            img = ImageTk.PhotoImage(img_file.resize((28,72)))
            pos = self.circles_positions[object_ids[0]]
            markerID = self.canvas.create_image(pos[0], pos[1], image=img)
            marker = markerID, img, pos
            self.land_markers.append(marker)

            self.controller.change_phase()
            can_attack = False
            for t in players[turn]._territories:
                if t.attackables():
                    can_attack = True
                    break
            if can_attack:
                self._show_skip_button()
            else:
                self.controller.change_phase()
                self.controller.switch_turn()
                self.is_new_turn = True
        elif self.controller.game_phase()[0] == 1: # attacking phase
            if self.attacker_choosed == None:
                if not territory.attackables():
                    return
                self.attacker_choosed = territory
                c_id = self.circles[territory.id()-1]
                pos = self.circles_positions[c_id]
                self.choice_arc = self.canvas.create_circle(pos[0], pos[1], NODE_SIZE+3,
                    width=4, outline=COLORS['REDY'])
                self._highlight_attackables(self.attacker_choosed)
                self.attacker_choosed = self.attacker_choosed

            else:
                if territory not in self.attacker_choosed.attackables():
                    return

                diff = self.attacker_choosed.n_armies - territory.n_armies - 1
                placed_armies = self._army_placement_window(diff)
                if placed_armies is None:
                    return
                players[turn].conquer(self.attacker_choosed, territory, placed_armies)
                c_id = self.circles[territory.id()-1]
                pos = self.circles_positions[c_id]
                for m in self.land_markers:
                    if m[-1][0] ==pos[0] and m[-1][1] ==pos[1]:
                        self.canvas.delete(m[0])
                        del m
                        break
                img_file = Image.open(STANDING_SOLJ.format(turn+1))
                img = ImageTk.PhotoImage(img_file.resize((28,72)))
                pos = self.circles_positions[object_ids[0]]
                markerID = self.canvas.create_image(pos[0], pos[1], image=img)
                marker = markerID, img, pos
                self.land_markers.append(marker)

                self.attacker_choosed = None
                self.canvas.delete(self.choice_arc)
                self._hide_skip_button()
                self.controller.change_phase()
                self.controller.switch_turn()
                self.is_new_turn = True



    def _create_canvas(self):
        self.canvas = Canvas(self.embed, highlightthickness=0,
            relief='ridge', bg=COLORS['BACKGROUND'])
        self.canvas.pack(fill="both", expand=True)
        # add custom functionss
        def _create_circle(x, y, r, **kwargs):
            return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
        self.canvas.create_circle = _create_circle

        def _create_circle_arc(x, y, r, **kwargs):
            return self.canvas.create_arc(x-r, y-r, x+r, y+r, **kwargs)
        self.canvas.create_circle_arc = _create_circle_arc
        
        # add event listeners
        self.canvas.bind('<Motion>', self._motion)
        self.canvas.last_object = None
        
        self.canvas.bind("<Button-1>", self._user_play)
        self.land_markers = []



    def _init_game(self):
        # self._splash_screen()
        Utility.play_sound(1)
        self._options_menu()
        self._create_canvas()
        self._skip_button()
        # self.screen.fill(BACKGROUND)
        self._legend()
        self._side_menu()
        # build graph
        self._build_graph()
        Utility.play_sound(0)


    def run(self):
        self._init_game()
        players = self.controller.players()
        self.is_new_turn = True
        self.is_agent_player = True
        self.attacker_choosed = None
        self.game_over = False
        while True:
            turn, gameover = self.controller.get_game_state()
            if not self.game_over and gameover:
                self.game_over = True
                
                header = "Player {} wins".format(turn+1);
                pls = self.controller.players()
                summary = "# of Turns: {}\nRemained Bonus{}".format(5,
                    pls[turn].armies)
                GameOverWindow(self.master, header, summary)
            
            self._side_menu_labels(turn, players)
            # check user type at each turn
            if self.is_new_turn:
                turn, _ = self.controller.get_game_state()
                self.is_new_turn = False
                if isinstance(players[turn], Agent): # player is an AI agent
                    players[turn].play()
                    self.is_agent_player = True
                    self.controller.switch_turn()
                    self._hide_skip_button()
                    self.is_new_turn = True
                else:
                    self.is_agent_player = False
                    if players[turn].armies == 0:
                        self.controller.change_phase()
                        self._show_skip_button()
            self.master.update() 
