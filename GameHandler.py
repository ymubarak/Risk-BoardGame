from Player import *
from Territory import *
from Continent import *
import Reader
from Agents import PassiveAgent, PacifistAgent

PHASES = ["Place Armies", "Attack!"]

class GameHandler():
    
    def __init__(self, file_path):
        self._turn = 0
        self._game_ended = False
        self._graph, self._continents = Reader.read_game(file_path)
        self._graph_size = len(self.graph())
        # players options
        self._player_types = ('Human', 'Passive Agent', 'Agressive Agent', 'Pacifist Agent',
            'Greedy Agent', 'A-Star Agent', 'A-Star-real-time Agent')
        self._game_phase = 0
        self.is_draw = False

    def create_players(self, type_1, type_2):
        p1 = None
        p2 = None
        # set player 1
        if type_1 == self._player_types[0]:
            p1 = Player()
        elif type_1 == self._player_types[1]:
            p1 = PassiveAgent.PassiveAgent(self)
        elif type_1 == self._player_types[2]:
            p1 = AgressiveAgent.AgressiveAgent(self)
        elif type_1 == self._player_types[3]:
            p1 = PacifistAgent.PacifistAgent(self)

        # set player 2
        if type_2 == self._player_types[0]:
            p2 = Player()
        elif type_2 == self._player_types[1]:
            p2 = PassiveAgent.PassiveAgent(self)
        elif type_2 == self._player_types[2]:
            p2 = AgressiveAgent.AgressiveAgent(self)
        elif type_2 == self._player_types[3]:
            p2 = PacifistAgent.PacifistAgent(self)
        
        self._players = [p1, p2]
        self._players[0].armies = 3
        self._players[1].armies = 3

    def switch_turn(self):
        if self._game_ended:
            return
        player_lands = len(set(self._players[self._turn]._territories))
        if player_lands == self._graph_size:
            self._game_ended = True
        
        for c in self._continents:
            if not (set(c.territories()) - set(self._players[0]._territories)):
                c.owner = self._players[0]
            elif not (set(c.territories()) - set(self._players[1]._territories)):
                c.owner = self._players[1]
            else:
                 c.owner = None
        
        self._turn = 1 if self._turn==0 else 0
        # phase 1
        self._players[self._turn].reinforce()
        for c in self._continents:
            if self._players[self._turn] == c.owner:
                c.reinforce_owner()

        no_owner = True
        for c in self._continents:
            if c.owner != None:
                no_owner = False
                break

        if (no_owner and
            self._players[0].armies == 0 and
            self._players[1].armies == 0 and
            not self.can_attack(self._players[0]) and 
            not self.can_attack(self._players[1])):
            self._game_ended = True
            self.is_draw = True

    def can_attack(self, player):
        can_attack = False
        for t in player._territories:
            if t.attackables():
                can_attack = True
                break
        return can_attack
    

    def change_phase(self):
        self._game_phase = 0 if self._game_phase==1 else 1
        return PHASES[self._game_phase]

    def game_phase(self):
        return self._game_phase, PHASES[self._game_phase]

    def get_game_state(self):
        return self._turn, self._game_ended

    def graph(self):
        return self._graph    

    def continents(self):
        return self._continents

    def player_types(self):
        return self._player_types

    def players(self):
        return self._players
    # for debugging purpose
    def print_state():
        space = "    "
        for i, p in enumerate(self._players):
            print("Player{}".format(i+1))
            print("{}Armies: {}".format(space, p.armies))
            print("{}Lands:".format(space))
            for t in p._territories:
                print("{} tid: {}".format(space*2, t.id))
                print("{}Armies: {}".format(space*3, t.n_armies))

