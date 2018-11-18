from Player import *
from Agents.Agent import Agent


class AgressiveAgent(Player, Agent):
	def __init__(self):
		Agent.__init__(self, "AgressiveAgent")
		Player.__init__(self)
		
	def place_armies(self):
		if self._armies == 0:
			return
		territory = None
		if not self._territories:
			max_bonus = -1
			max_cont = None
			for cont in self.controller.continents():
				if max_bonus < cont.bonus():
					max_bonus = cont.bonus()
					max_cont = cont
			territory = max_cont.territories()[0]
		else:
			max_armies = sorted(self._territories, key=lambda x: x.n_armies, reverse=True)
			min_vertex_numbers = sorted(min_armies, key=lambda x: x.id())
			territory = min_vertex_numbers[0]

		territory.n_armies += self._armies
		self._armies = 0
		self.add_territory(territory)


	def attack(self):
		# TODO
		pass