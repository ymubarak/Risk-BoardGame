from Player import *
from Agents.Agent import Agent


class PacifistAgent(Player, Agent):
	def __init__(self):
		Agent.__init__(self, "PacifistAgent")
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
			min_armies = sorted(self._territories, key=lambda x: x.n_armies)
			min_vertex_numbers = sorted(min_armies, key=lambda x: x.id())
			territory = min_vertex_numbers[0]

		territory.n_armies += self._armies
		self._armies = 0
		self.add_territory(territory)


	def attack(self):
		can_attack = filter(lambda x: len(x.attackables()) > 0, self._territories)
		min_loss = sorted(can_attack, key=lambda x: min([t.n_armies for t in x.attackables()]))
		min_vertex_numbers = sorted(min_armies, key=lambda x: x.id())
		if len(min_vertex_numbers) > 0:
			attacker = min_vertex_numbers[0]
			candidates = attacker.attackables()
			attacked = candidates[0]
			min_loss = candidates[0].n_armies
			for t in candidates:
				if t.n_armies < min_loss:
					min_loss = t.n_armies
					attacked = t

			self.conquer(attacker, attacked, 1) #TODO: why 1?