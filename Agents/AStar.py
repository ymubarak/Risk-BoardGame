from Player import *
from Territory import *
from Continent import *
from GameHandler import *
from Agents.Agent import Agent
from Agents.InformedSearch import InformedSearch
from TreeNode import *
from GameState import *
import copy


class AStar(Player, Agent):
    def __init__(self, controller, pid):
        Player.__init__(self, pid)
        Agent.__init__(self, "Astar Agent")
        self.controller = controller
        self.attacker = None
        self.placement = None
        self.attacked = None

    
    def heuristic(self, state):
        territories_ratio = state.territories_ration_per_continent()
        armies_ratio = 1- state.armies / (state.armies + state.opponent_armies)
        h = armies_ratio * territories_ratio
        return h 

    def cost(self, state):
        cost = 0
        while state.parent != None:
            cost +=1
        return cost


    def get_territory_by_id(self, tid):
        for t in self._territories:
            if t.id() == tid:
                return t

    def place_armies(self):
        agent_action = {}

        player_copy = copy.deepcopy(self)
        cont_copy = copy.deepcopy(self.controller.continents())
        init_state = GameState(player_copy, cont_copy)
        self.informed_search = InformedSearch(init_state, self.controller)

        
        self.informed_search.set_heuristic(self.heuristic)
        self.informed_search.set_cost(self.cost)
        next_state = self.informed_search.get_search_result()
        if next_state != None:
            attacker_id, attacked_id, placement = next_state
            self.attacker = self.get_territory_by_id(attacker_id)
            self.attacked = self.get_territory_by_id(attacked_id)
            self.placement = placement
            if self.armies != 0:
                agent_action['placement'] = (attacker, self._armies)
        elif self.armies != 0:
            self.attacker = None
            self.placement = None
            self.attacked = None
            max_armies = sorted(self._territories, key=lambda x: x.n_armies, reverse=True)
            for t in max_armies:
                for nbr in t.neighbors():
                    if nbr.owner != t.owner:
                        self.attacker = t
            agent_action['placement'] = (self.attacker, self._armies)
            

        return agent_action

    def attack(self):
        agent_action = {}
        if self.attacked == None and self.attacker != None:
                if self.attacker.attackables():
                    self.attacked = self.attacker.attackables()[0]
                    self.placement = (self.attacker.n_armies - self.attacked.n_armies)//2
                else:
                    self.attacker = None

        if self.attacker != None:
            agent_action['attack'] = (self.attacker, self.attacked, self.placement)    
        return agent_action