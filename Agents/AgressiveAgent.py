from Player import *
from Agents.Agent import Agent


class AgressiveAgent(Player, Agent):
	def __init__(self):
		Agent.__init__(self, "AgressiveAgent")
		Player.__init__(self)
		
	def place_armies(self):
		max_armies = sorted(self._territories, key=lambda x: x.n_armies, reverse=True)
		min_vertex_numbers = sorted(min_armies, key=lambda x: x.id())
		min_vertex_numbers[0].n_armies += self._armies
		self._armies = 0


	def attack(self):
		# TODO
		pass