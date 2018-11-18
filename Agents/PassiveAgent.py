from Player import *
from Agents.Agent import Agent


class PassiveAgent(Player, Agent):
	def __init__(self, controller):
		Agent.__init__(self, "PassiveAgent")
		Player.__init__(self)
		self.controller = controller
		
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
			min_armies = sorted(self._territories, key=lambda x: x.n_armies)
			min_vertex_numbers = sorted(min_armies, key=lambda x: x.id())
			territory = min_vertex_numbers[0]

		territory.n_armies += self._armies
		self._armies = 0
		self.add_territory(territory)