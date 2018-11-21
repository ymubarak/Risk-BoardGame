from Player import *
from Agents.Agent import Agent


class AgressiveAgent(Player, Agent):
    def __init__(self, controller):
        Agent.__init__(self, "PassiveAgent")
        Player.__init__(self)
        self.controller = controller
        
    def place_armies(self):
        agent_action = {}
        if self._armies == 0:
            agent_action['placement'] =()
            return agent_action
        territory = None
        if not self._territories:
            max_bonus = -1
            max_cont = None
            for cont in self.controller.continents():
                if cont.owner != None:
                    continue
                if max_bonus < cont.bonus():
                    max_bonus = cont.bonus()
                    max_cont = cont
            for t in max_cont.territories():
                if t.owner is None:
                    territory = t
                    break
        else:
            max_armies = sorted(self._territories, key=lambda x: x.n_armies, reverse=True)
            max_army = max_armies[0].n_armies
            stop_point = 1
            for i in range(1, len(max_armies)):
                if max_armies[i].n_armies < max_army:
                    stop_point = i
                    break
            max_armies = max_armies[:stop_point]
            min_vertex_numbers = sorted(max_armies, key=lambda x: x.id())
            territory = min_vertex_numbers[0]

        
        agent_action['placement'] = (territory, self._armies)
        return agent_action


    def attack(self):

        agent_action = {}

        for c in self.controller.continents():
            if c.owner != self and c.owner != None:
                for t in c._territories:
                    for nbr in t.neighbors():
                        if t in nbr.attackables():
                            placement = nbr.n_armies - t.n_armies
                            agent_action['attack'] = (nbr, t, placement - 1)
                            return agent_action

        for t in self._territories:
            candidates = t.attackables()
            if candidates:
                attacked = candidates[0]
                placement = t.n_armies - attacked.n_armies 
                agent_action['attack'] = (t, attacked, placement - 1)
                return agent_action

        return agent_action







