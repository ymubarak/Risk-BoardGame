from Player import *
from Territory import *
from Continent import *
from GameHandler import *
from Agents.Agent import Agent

class HillClimbing(Player, Agent):
    def __init__(self, controller, pid):
        Player.__init__(self, pid)
        Agent.__init__(self, "HillClimbing")
        self.controller = controller
        # opponents nearest territories
        self._targets = {}
        self.attacker = None
        self.attacked = None

    # the more an opponent territory has attackers, the more weight it gains
    def increase_key(self, k):
        if k in self._targets:
            self._targets[k] += 1
        else:
            self._targets[k] = 1

    def search(self):
        self._targets = {}
        for t in self._territories:
            for nb in t._neighbors:
                if nb.owner != self and nb.owner != None:
                    self.increase_key(nb)

        self._targets = sorted(self._targets.items(), key=lambda kv: kv[1])
        print("===================\n")
        print(self._targets)

    def discover(self):
        # run search functions to find all targets
        self.search()

        # determine the best attacker
        # we assumed it's the one has the max number of armies
        max_armies = sorted(self._territories, key=lambda x: x.n_armies, reverse=True)

        # Among possible candidate opponent territories [targets], choose the territory with 
        # the maximum possible armies to attack it
        for (candidate, weight) in self._targets:
            for attacker in max_armies:
                if candidate in attacker.attackables():
                    self.attacker = attacker
                    self.attacked = candidate
                    break
            else:
                continue
            break


    def place_armies(self):
        agent_action = {}
        if self._armies == 0:
            return agent_action
        
        territory = None
        if not self._territories:
            continents = self.controller.continents()
            territory = self._init_placement(continents)
        else:
            self.discover()
            if (self.attacker != None):
                territory = self.attacker
            else: # can not attack
                max_armies = sorted(self._territories, key=lambda x: x.n_armies, reverse=True)
                territory = max_armies[0]
        
        agent_action['placement'] = (territory, self._armies)
        return agent_action

    def attack(self):
        agent_action = {}
        if (self.attacker != None and self.attacked != None and (self.attacked in self.attacker.attackables())):
            placement = self.attacker.n_armies - self.attacked.n_armies
            agent_action['attack'] = (self.attacker, self.attacked, placement - 1)
        return agent_action