from Player import *
from Territory import *
from Continent import *
from GameHandler import *
from Agents.Agent import Agent
from TreeNode import *
import heapq





class AStarRealTime(Player, Agent):
    """
    f(x) = g(x)+h(x)
    where g(x) is number of taken turns till reaching this node
    """
    def __init__(self, controller):
        Player.__init__(self)
        Agent.__init__(self, "AStarRealTime")
        self.controller = controller
        self.attacked = None
        self.attacker = None

    # calculate h for the Territory
    def h_function(self, attackers, target):
        cnt = 0
        for nbr in target.neighbors():
            if nbr in attackers:
                cnt += 1
        return (1.0 - cnt/len(target.neighbors()))

    def find_targets(self, attackers):
        targets = []
        for t in self.controller.graph().values():
            if t not in attackers:
                targets.append(t)
        return targets

    def build_tree_node(self, attackers, targets_temp, g_cost=1, parent=None):
        targets = []
        if not targets_temp:
            return targets
        for t in targets_temp:
            # put 0 for g function and None for parent node
            node = TreeNode(t, g_cost, self.h_function(attackers, t), parent)
            targets.apped(node)
        return targets

    def find_attacked(self, node):
        p = node
        while p.parent != None:
            p = p.parent
        return p

    def check_attackability(self, targets):
        new_targets = []
        if not targets:
            return new_targets
        for t in targets:
            for nbr in t.neighbors():
                if t in nbr.attackables():
                    new_targets.append(t)
                    break
        return new_targets

    def attacked_search(self):
        attackers = self._territories

        targets_temp1 = self.find_targets(attackers)
        targets_temp2 = self.check_attackability(targets_temp1)
        if not targets_temp2:
            max_armies = sorted(targets_temp1, key=lambda x: x.n_armies, reverse=False)
            for t in max_armies:
                for nbr in t.neighbors():
                    if nbr.owner != t.owner:
                        self.attacked = t
                        self.attacker = nbr
                        return self.attacked

        targets_temp = targets_temp2
        # else, build your tree search
        targets = self.build_tree_node(attackers, targets_temp)
        targets = sort(targets)
        min_node = None

        # if targets is empty, then we reach our goal
        while targets:
            min_node = targets[0]
            attackers.append(min_node.t)
            targets.remove(min_node)

            succesors = self.find_succesors(min_node.t, attackers)
            succesors = self.build_tree_node(attackers, succesors, min_node)

            for suc in succesors:
                for node in targets:
                    if suc.t == node.t:
                        if suc.g < node.t:
                            targets.append(suc)
                            targets.remove(node)

            targets = sort(targets)

        attacked = self.find_attacked(min_node)

        return attacked

    def find_succesors(self, t, attackers):
    	succesors = []
    	for nbr in t.neighbors():
    		if nbr not in attackers:
    			succesors.append(nbr)
    	return succesors


    def determine_attacker(self, attacked):
        if not attacked:
            return None
        for attacker in attacked.neighbors():
            if attacked in attacker.attackables():
                return attacker
        return None

    def determine_play():
        self.attacked = self.attacked_search()
        self.attacker = self.determine_attacker(self.attacked)

    def place_armies(self):
        self.determine_play()
        agent_action = {}
        if self.attacker != None:
            agent_action['placement'] = (self.attacker, self._armies)
        else:
            max_armies = sorted(self._territories, key=lambda x: x.n_armies, reverse=True)
            t = max_armies[0]
            agent_action['placement'] = (t, self._armies)
        return agent_action

    def attack(self):
        self.determine_play()
        agent_action = {}
        if (self.attacker != None and self.attacked != None and (self.attacked in self.attacker.attackables())):
            placement = self.attacker.n_armies - self.attacked.n_armies
            agent_action['attack'] = (self.attacker, self.attacked, placement - 1)
    return agent_action