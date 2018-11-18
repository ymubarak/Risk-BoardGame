from Player import *
from Agents.Agent import Agent


class PacifistAgent(Player, Agent):
	def __init__(self, controller):
		Agent.__init__(self, "PassiveAgent")
		Player.__init__(self)
		self.controller = controller
		
	def place_armies(self):
		agent_action = {}
		if self._armies == 0:
			agent_action['placement'] =()
			return agent_action
		territory = None
		if not self._territories:
			max_bonus = -1
			max_cont = None
			for cont in self.controller.continents():
				if cont.owner != None:
					continue
				if max_bonus < cont.bonus():
					max_bonus = cont.bonus()
					max_cont = cont
			for t in max_cont.territories():
				if t.owner is None:
					territory = t
					break
		else:
			min_armies = sorted(self._territories, key=lambda x: x.n_armies)
			min_loss = min_armies[0].n_armies
			stop_point = 1
			for i in range(1, len(min_armies)):
				if min_armies[i].n_armies > min_loss:
					stop_point = i
					break
			min_armies = min_armies[:stop_point]
			min_vertex_numbers = sorted(min_armies, key=lambda x: x.id())
			territory = min_vertex_numbers[0]

		
		agent_action['placement'] = (territory, self._armies)
		return agent_action


	def attack(self):
		agent_action = {}
		can_attack = list(filter(lambda x: len(x.attackables()) > 0, self._territories))
		if not can_attack:
			return agent_action
		min_armies = sorted(can_attack, key=lambda x: min([t.n_armies for t in x.attackables()]))

		min_loss = min([t.n_armies for t in min_armies[0].attackables()])
		stop_point = 1
		for i in range(1, len(min_armies)):
			if min([t.n_armies for t in min_armies[i].attackables()]) > min_loss:
				stop_point = i
				break
		min_armies = min_armies[:stop_point]
		min_vertex_numbers = sorted(min_armies, key=lambda x: x.id())

		attacker = min_vertex_numbers[0]
		candidates = attacker.attackables()
		attacked = candidates[0]
		min_loss = candidates[0].n_armies
		for t in candidates:
			if t.n_armies < min_loss:
				min_loss = t.n_armies
				attacked = t

		agent_action['attack'] = (attacker, attacked, 1) #TODO: why 1?

		return agent_action