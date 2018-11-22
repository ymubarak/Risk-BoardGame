from Player import *
from Territory import *
from Continent import *
from GameHandler import *
from Agents.Agent import Agent



class HillClimbing(Player, Agent):
    def __init__(self, controller):
        Player.__init__(self)
        Agent.__init__(self, "GreedyAgent")
        # opponents nearest territories
        self.controller = controller
        self._targets = {}
        self.attacker = None
        self.attacked = None

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

        for (attacked, weight) in self._targets:

            for attacker in max_armies:
                if attacked in attacker.attackables():
                    self.attacker = attacker
                    self.attacked = attacked
                    break
            else:
                continue
            break


    def place_armies(self):
        self.discover()
        agent_action = {}
        if (self.attacker != None):
            agent_action['placement'] = (self.attacker, self._armies)
        else:
            max_armies = sorted(self._territories, key=lambda x: x.n_armies, reverse=True)
            t = max_armies[0]
            agent_action['placement'] = (t, self._armies)
        return agent_action

    def attack(self):
        agent_action = {}
        if (self.attacker != None and self.attacked != None and (self.attacked in self.attacker.attackables())):
            placement = self.attacker.n_armies - self.attacked.n_armies
            agent_action['attack'] = (self.attacker, self.attacked, placement - 1)
        return agent_action