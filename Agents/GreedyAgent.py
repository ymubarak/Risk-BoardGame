from Player import *
from Territory import *
from Continent import *
from GameHandler import *


class GreedyAgent(Player, Agent):
	"""Greedy search agent is an agent that
	picks the move with best immediate heuristic value.

	our assumed heuristic function has the following priorities:
	1. own a continent
	2. conquer an oponent's continent
	3. attack other terrotries nearest to your continent

	that all can be achieved using a heauristic function like h(x)=sum(opponent's neighbors)

	note: place armies on the selceted attacker
	"""
	def __init__(self):
		Player.__init__(self)
		Agent.__init__(self, "GreedyAgent")
		# opponents nearest territories
		self._targets = {}

	def increase_key(k):
        if k in _targets:
            self._targets[k] += 1
        else:
            self._targets[k] = 1

	def search():
		for t in territories:
			nbs = t.neighbors
			for nb in nbs:
				if nb.owner != Player:
					self.increase_key(nb)

	    self._targets = sorted(self._targets.items(), key=lambda kv: kv[1])

    def place_armies(self):
    	pass

	def place_armies(self, attacker):
		# placement
		attacker.n_armies = self.armies
		self._armies = 0

	def attack(self):
		# run search functions to find all targets
		self.search()

		# determine the best attacker
		# we assumed it's the one has the max number of armies
		max_armies = sorted(self.territories, key=lambda x: x.n_armies, reverse=True)

		for attacked in list(_targets.keys()):

            attacker_index = -1
		    for i in range(len(max_armies)):
			    if t in attacked[i].neighbors:
				    attacker_index = i

		    attacker = max_armies[attacker_index]

			attackables_territories = attacker.attackables()
		        if attacked in attackables_territories:
		        	# take actions
		        	# 1. Do placement
		        	self.place_armies(attacker)
		        	# 2. attacking
		        	self.conquer(attacker, attacked, placement)
		        	break
		    else:
                continue
            break














		
		