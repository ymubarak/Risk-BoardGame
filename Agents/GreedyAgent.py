from Player import *
from Territory import *
from Continent import *
from GameHandler import *
from Agents.Agent import Agent
from TreeNode import *





class GreedyAgent(Player, Agent):
    """
    A greedy agent is the agent that picks the move with best immediate heuristic value.
    heuristic(x) = 1 - (#edges connect to opponents vertices / #total edges of x)
    to achieve that we have two lists: t_mine and t_oppo as my territoris and 
    opponent's territories respectivly.

    """
    def __init__(self, controller):
        Player.__init__(self)
        Agent.__init__(self, "GreedyAgent")
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
        for t in self.controller.graph():
            if t not in attackers:
                targets.append(t)
        return targets

    def build_tree_node(self, attackers, targets_temp, parent=None):
        targets = []
        for t in targets_temp:
            # put 0 for g function and None for parent node
            node = TreeNode(t, 0, self.h_function(attackers, t), parent)
            targets.apped(node)

    def find_attacked(self, TreeNode):
        p = TreeNode
        while p.parent != None:
            p = TreeNode.parent
        return p

    def check_attackability(self, targets):
        new_targets = []
        for t in targets:
            for nbr in t.neighbors():
                if t in nbr.attackables():
                    new_targets.append(t)
                    break

    def attacked_search(self):
        attackers = self._territories

        targets_temp = self.find_targets(attackers)
        targets_temp = self.check_attackability(targets_temp)


        targets = self.build_tree_node(attackers, targets_temp)
        targets = sort(targets)

        min_node = None

        # if targets is empty, then we reach our goal
        while targets:
            min_node = targets[0]
            attackers.append(min_node.t)
            targets_temp.remove(min_node.t)

            targets = self.build_tree_node(attackers, targets_temp, min_node)
            targets = sort(targets)

        attacked = self.find_attacked(min_node)

        return attacked

    def determine_attacker(self, attacked):
        for attacker in attacked.neighbors():
            if attacked in attacker.attackables():
                return attacker
        return None

    def place_armies(self):

        self.attacked = self.attacked_search()
        self.attacker = self.determine_attacker(self.attacked)

        agent_action = {}
        if (self.attacker != None):
            agent_action['placement'] = (self.attacker, self._armies)
        else:
            max_armies = sorted(self._territories, key=lambda x: x.n_armies, reverse=True)
            agent_action['placement'] = (max_armies[0], self._armies)
        return agent_action

    def attack(self):
        agent_action = {}
        if (self.attacker != None and self.attacked != None and (self.attacked in self.attacker.attackables())):
            placement = self.attacker.n_armies - self.attacked.n_armies
            agent_action['attack'] = (self.attacker, self.attacked, placement - 1)
        return agent_action
        