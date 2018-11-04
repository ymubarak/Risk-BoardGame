from Player import *
from Territory import *
from Continent import *
import Reader
from Agents import PassiveAgent, PacifistAgent

class GameHandler():
    
    def __init__(self, file_path):
        self._turn = 0
        self._game_ended = False
        self._graph, self._continents = Reader.read_game(file_path)
        self._graph_size = len(self.graph())
        # players options
        self._player_types = ('Human', 'Passive Agent', 'Agressive Agent', 'Pacifist Agent',
            'Greedy Agent', 'A-Star Agent', 'A-Star-real-time Agent')
        self._players = [Player(),PassiveAgent.PassiveAgent()]
        self._players[0].armies = 3
        self._players[1].armies = 3

    
    def switch_turn(self):
        self._turn = 1 if self._turn==0 else 0
        # phase 1
        self._players[self._turn].reinforce()
        for c in self._continents:
            if self._players[self._turn] == c.owner:
                c.reinforce_owner()

        # phase 2
        # if turn == 0 (human turn)
            # wait for gui interaction/decission
            # - place armies
            # - attack ==> choose new placement
        # else:
            # TODO: choose an agent to play 

        player_lands = len(set(self._players[self._turn]._territories))
        if player_lands == self._graph_size:
            self._game_ended = True

    
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

