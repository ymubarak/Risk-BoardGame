import os
import time
import threading
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
DISTANCE = 120

FPS = 14


# paths
STANDING_SOLJ = "media/images/standing{}.png"
FIGHTING_SOLJ = "media/images/fighting{}.png"
AX = "media/images/ax.png"

lock = threading.Lock()

class Game(Frame):
    def __init__(self, controller):
        super().__init__() 
        if not isinstance(controller, GameHandler):
            raise TypeError("Invalid controller, Game object must be supplied with a `GameHandler` object")
        
        self.controller = controller
        self.master.title(TITLE)
        self.master.configure(background = "red")
        self.master["bg"] = "red"
        self.master.minsize(WIDTH, HEIGHT)
        self.master.attributes("-fullscreen", True) 

        # self.master.maxsize(WIDTH+SIDE_MENU_WIDTH, HEIGHT)

        self.embed = tk.Frame(self.master) #creates embed frame for pygame window
        self.embed.grid() # Adds grid
        self.embed.pack(side='left', fill='both', expand=True) # packs window to the left
        os.environ['SDL_WINDOWID'] = str(self.embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        # create pygame
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode()
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
        SCREEN_SIZE = self.master.winfo_width(), self.master.winfo_height()
        sp_screen = SplashScreen(self.screen, SCREEN_SIZE)


    def _army_placement_window(self, armies):
        placment_window = ArmyPlacementWindow(self.master, armies)
        self.master.wait_window(placment_window.top)
        if placment_window.value_set:
            return int(placment_window.num_armies)
    
    def _skip_button(self):
        width = 80
        height = 40
        x1 = self.master.winfo_width()/2 - width/2
        y1 = -height
        x2 = x1 + width
        y2 = 0
        top_padding = 20
        left_padding = 39

        self.skip_button_rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLORS['REDY'])
        self.skip_button_txt = self.canvas.create_text(x1+left_padding, y1+top_padding,
         text="Skip", fill="white", font=(None, 14))
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
    
    
    def _phase_popup(self, phase_name):
        # lock.acquire() # will block if lock is already held

        font_size = 40
        left_padding = font_size/2
        x = self.master.winfo_width()/2
        y = 0.05*self.master.winfo_height()
        top_padding = 20

        turn, _ = self.controller.get_game_state()
        popup_text = "Player{} : {}".format(turn+1, phase_name)
        txt = self.canvas.create_text(x, y,
         text=popup_text, fill="white", font=(None, font_size))

        self.master.update()
        wait_time = 0.5 # in seconds
        time.sleep(wait_time)
        self.canvas.delete(txt)
        time.sleep(wait_time)
        
        # def remove_pop_up():
        #     time.sleep(wait_time)
        #     self.canvas.delete(txt)
        
        # self.master.after(1, lambda: remove_pop_up())
        # lock.release()
        pass
    
    
    def _build_graph(self):
        # variables
        self.graph_size = len(self.controller.graph())
        global NODE_SIZE
        NODE_SIZE = NODE_SIZE/ (self.graph_size)**0.5
        scale_factor = 2.25*DISTANCE + DISTANCE/(self.graph_size)**0.5

        G = nx.Graph()
        for key in self.controller.graph().keys():
            G.add_node(key)

        for node in self.controller.graph().values():
            for nb in node.neighbors():
                G.add_edge(node.id(), nb.id())
        
        
        # organize nodes in layout
        positions = None
        if self.graph_size <= 5:
            positions = nx.circular_layout(G)
            scale_factor *= 0.75
            NODE_SIZE *= 1.25
        else:
            positions = nx.fruchterman_reingold_layout(G, k=10*NODE_SIZE)
        
        pos = [(p*scale_factor).astype("int") for p in positions.values()]
        min_x = min([p[0] for p in pos])
        max_x = max([p[0] for p in pos])
        mid_x = (max_x+min_x)/2
        x_displacement = self.master.winfo_width()/2 - mid_x

        min_y = min([p[1] for p in pos])
        max_y = max([p[1] for p in pos])
        mid_y = (max_x+min_y)/2
        y_displacement = self.master.winfo_height()/2 - mid_y

        pos = [(p[0]+x_displacement,p[1]+y_displacement) for p in pos]

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
        for i, p in enumerate(pos, start=1):
            # node color
            color = None
            for c in self.controller.continents():
                t = self.controller.graph()[i]
                if c.has_territory(t):
                    color = Colors.to_hex(c.color())
                    break
            object_id = self.canvas.create_circle(p[0], p[1], NODE_SIZE, fill=color, width=2)
            self.circles.append(object_id)
            self.circles_positions[object_id] = (p[0], p[1])
            # Utility.draw_text(self.screen, str(i), p[0], p[1],size=NODE_SIZE+1, center=True)
        
        scale = 720/ (2*NODE_SIZE)
        scale_y = int(720/scale)
        scale_x = int(280/scale)
        ax_scale = int(NODE_SIZE)

        self.icons = [Image.open(STANDING_SOLJ.format(1)).resize((scale_x, scale_y)),
                        Image.open(STANDING_SOLJ.format(2)).resize((scale_x, scale_y)),
                        Image.open(AX).resize((ax_scale, ax_scale))]

        for i, p in enumerate(self.controller.players()):
            for t in p._territories:
                img = ImageTk.PhotoImage(self.icons[i])
                pos = self.circles_positions[self.from_ter_to_objID(t)]
                markerID = self.canvas.create_image(pos[0], pos[1], image=img)
                marker = markerID, img, pos
                self.land_markers.append(marker)
    
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
    

    def handle_placement(self, players, turn, territory):
        other_player = 0 if turn==1 else 1
        if players[other_player].has_territory(territory):
            return
        
        #placed_armies = self._army_placement_window(players[turn].armies)
        #if placed_armies is None:
        #    return
        territory.n_armies+= players[turn].armies
        players[turn].armies = 0
        if not players[turn].has_territory(territory):
            players[turn].add_territory(territory)
        
        img = ImageTk.PhotoImage(self.icons[turn])
        pos = self.circles_positions[self.from_ter_to_objID(territory)]
        markerID = self.canvas.create_image(pos[0], pos[1], image=img)
        marker = markerID, img, pos
        self.land_markers.append(marker)

        phn = self.controller.change_phase()
        self._phase_popup(phn)
        self.check_attackability(players[turn])
        
    
    def handle_attack(self, players, turn, territory):
        if self.attacker_choosed == None:
            if not territory.attackables():
                return
            self.attacker_choosed = territory
            c_id = self.circles[territory.id()-1]
            pos = self.circles_positions[c_id]
            self.choice_arc = self.canvas.create_circle(pos[0], pos[1], NODE_SIZE+3,
                width=4, outline=COLORS['REDY'])
            self._highlight_attackables(self.attacker_choosed)

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
            
            img = ImageTk.PhotoImage(self.icons[turn])
            pos = self.circles_positions[self.from_ter_to_objID(territory)]
            markerID = self.canvas.create_image(pos[0], pos[1], image=img)
            marker = markerID, img, pos
            self.land_markers.append(marker)

            self.attacker_choosed = None
            self.canvas.delete(self.choice_arc)
            self._hide_skip_button()
            self.controller.switch_turn()
            _, gameover = self.controller.get_game_state()
            if not gameover:
                phn = self.controller.change_phase()
                self._phase_popup(phn)
            self.is_new_turn = True
            self.ax_markers = []
    
    
    def _show_attack_ticks(self, player):
        for t in player._territories:
            if t.attackables():
                img = ImageTk.PhotoImage(self.icons[2])
                objID = self.from_ter_to_objID(t)
                coords = self.canvas.coords(objID)
                x = coords[2] - (coords[2]-coords[0])*0.2
                y = coords[1] + (coords[3]-coords[1])*0.1

                markerID = self.canvas.create_image(x, y, image=img)
                marker = markerID, img
                self.ax_markers.append(marker)

    def check_attackability(self, player):
            can_attack = False
            for t in player._territories:
                if t.attackables():
                    can_attack = True
                    self._show_attack_ticks(player)
                    break
            if can_attack:
                self._show_skip_button()
            else:
                self.ax_markers = []
                self.controller.switch_turn()
                phn = self.controller.change_phase()
                self._phase_popup(phn)
                self._hide_skip_button()
                self.is_new_turn = True

    def from_objID_to_ter(self, object_id):
        index = self.circles.index(object_id)
        territory = self.controller.graph()[index+1]
        return territory

    def from_ter_to_objID(self, territory):
        object_id = None
        index = -1
        for i in range(1, self.graph_size+1):
            if self.controller.graph()[i] == territory:
                index = i-1
                break

        object_id = self.circles[index]
        return object_id

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
            self.controller.switch_turn()
            phn = self.controller.change_phase()
            self._phase_popup(phn)
            self.is_new_turn = True
            self.attacker_choosed = None
            self.ax_markers = []
            return
        
        if object_ids[0] not in self.circles:
            return
        
        territory = self.from_objID_to_ter(object_ids[0])
        turn, _ = self.controller.get_game_state()
        players = self.controller.players()
        if self.controller.game_phase()[0] == 0: # place armies
            self.handle_placement(players, turn, territory)
            
        elif self.controller.game_phase()[0] == 1: # attacking phase
            self.handle_attack(players, turn, territory)



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
        
        
        def sign(n):
            if n > 0: return 1
            elif n < 0: return -1
            return 0
        
        def _moveloop(object_id, tomovex, tomovey, wait_time=5):
            if not tomovex and not tomovey:
                return  # Break the loop
            
            self.canvas.move(object_id, sign(tomovex), sign(tomovey))
            newx = (abs(tomovex) - 1) * sign(tomovex)
            newy = (abs(tomovey) - 1) * sign(tomovey)

            self.master.after(wait_time, lambda: _moveloop(object_id, newx, newy,wait_time))
        self.canvas.animate = _moveloop

        # add event listeners
        self.canvas.bind('<Motion>', self._motion)
        self.canvas.last_object = None
        
        self.canvas.bind("<Button-1>", self._user_play)
        self.land_markers = []
        self.ax_markers = []



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
        # Utility.play_sound(0)

    def handle_game_over(self, turn):
        header = None
        summary = None
        pls = self.controller.players()
        if self.controller.is_draw:
            header = "Draw !"
            summary = "Player1 Turns: {}\t|\tPlayer2 Turns: {}\n"\
            "Player1 Bonus: {}\t|\tPlayer2 Bonus: {}\n".format(self.controller.num_of_turns, self.controller.num_of_turns,
                        pls[0].armies, pls[1].armies)
        else:
            winner = 0 if turn==1 else 1
            num_of_turns = self.controller.num_of_turns # (self.controller.num_of_turns+1)//2
            header = "Player {} wins".format(winner+1);
            summary = "# of Turns: {}\nRemained Bonus: {}".format(num_of_turns,
                        pls[winner].armies)
        
        go = GameOverWindow(self.master, header, summary)
        self.master.wait_window(go.top)
        if go.play_again:
            self._init_game()
            self.game_over = False
        else:
            self.master.destroy()


    
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
                self.handle_game_over(turn)
                
            if self.game_over:
                self.master.update()
                continue
            
            self._side_menu_labels(turn, players)
            self.master.update() 

            # check user type at each turn
            if self.is_new_turn:
                turn, game_over = self.controller.get_game_state()
                self.is_new_turn = False
                wait_time = 1
                if isinstance(players[turn], Agent): # player is an AI agent
                    self.is_agent_player = True
                    time.sleep(wait_time)
                    agent_action = players[turn].place_armies()
                    if agent_action.get('placement', ()):
                        territory = agent_action['placement'][0]
                        placed_armies = agent_action['placement'][1]
                        territory.n_armies+= placed_armies
                        players[turn].armies -= placed_armies
                        if not players[turn].has_territory(territory):
                            players[turn].add_territory(territory)
                        
                        img = ImageTk.PhotoImage(self.icons[turn])
                        pos = self.circles_positions[self.from_ter_to_objID(territory)]
                        markerID = self.canvas.create_image(pos[0], pos[1], image=img)
                        marker = markerID, img, pos
                        self.land_markers.append(marker)
                        self.master.update()

                    
                    phn = self.controller.change_phase()
                    self._phase_popup(phn)
                    time.sleep(wait_time)

                    agent_action = players[turn].attack()
                    if agent_action.get('attack', ()):
                        self._show_attack_ticks(players[turn])
                        attacker = agent_action['attack'][0]
                        attacked = agent_action['attack'][1]
                        placed_armies = agent_action['attack'][2]
                        self.attacker_choosed = attacker
                        c_id = self.circles[self.attacker_choosed.id()-1]
                        pos = self.circles_positions[c_id]
                        self.choice_arc = self.canvas.create_circle(pos[0], pos[1], NODE_SIZE+3,
                            width=4, outline=COLORS['REDY'])
                        self._highlight_attackables(self.attacker_choosed)
                        
                        self.master.update()
                        time.sleep(wait_time)

                        players[turn].conquer(self.attacker_choosed, attacked, placed_armies)
                        c_id = self.circles[attacked.id()-1]
                        pos = self.circles_positions[c_id]
                        for m in self.land_markers:
                            if m[-1][0] ==pos[0] and m[-1][1] ==pos[1]:
                                self.canvas.delete(m[0])
                                del m
                                break
                        img = ImageTk.PhotoImage(self.icons[turn])
                        pos = self.circles_positions[self.from_ter_to_objID(attacked)]
                        markerID = self.canvas.create_image(pos[0], pos[1], image=img)
                        marker = markerID, img, pos
                        self.land_markers.append(marker)

                        self.attacker_choosed = None
                        self.canvas.delete(self.choice_arc)
                        self.master.update()                     

                    self._hide_skip_button()
                    self.controller.switch_turn()
                    _ , gameover = self.controller.get_game_state()
                    if not gameover:
                        phn = self.controller.change_phase()
                        self._phase_popup(phn)
                    phn = self.controller.change_phase()
                    self._phase_popup(phn)
                    self.is_new_turn = True
                    self.ax_markers = []

                elif not game_over:
                    self.is_agent_player = False
                    if players[turn].armies == 0:
                        phn = self.controller.change_phase()
                        self._phase_popup(phn)
                        self._show_skip_button()
                        self.check_attackability(players[turn])
            self.master.update() 
