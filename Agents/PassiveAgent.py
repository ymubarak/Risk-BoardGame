from Player import *
from Agents.Agent import Agent


class PassiveAgent(Player, Agent):
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
