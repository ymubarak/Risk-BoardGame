from Player import *
from Agents.Agent import Agent


class PassiveAgent(Player, Agent):
	def __init__(self):
		Agent.__init__(self, "PassiveAgent")
		Player.__init__(self)
		
	def place_armies(self):
		min_armies = sorted(self._territories, key=lambda x: x.n_armies)
		min_vertex_numbers = sorted(min_armies, key=lambda x: x.id())
		min_vertex_numbers[0].n_armies += self._armies
		self._armies = 0