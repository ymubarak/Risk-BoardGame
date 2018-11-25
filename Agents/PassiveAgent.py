from Player import *
from Agents.Agent import Agent


class PassiveAgent(Player, Agent):
	def __init__(self, controller, pid):
		Agent.__init__(self, "PassiveAgent")
		Player.__init__(self, pid)
		self.controller = controller
	
	def place_armies(self):
		agent_action = {}
		if self._armies == 0:
			agent_action['placement'] =()
			return agent_action
		territory = None
		if not self._territories:
			continents = self.controller.continents()
			territory = self._init_placement(continents)
		else:
			min_armies = sorted(self._territories, key=lambda x: x.n_armies)
			min_army = min_armies[0].n_armies
			stop_point = 1
			for i in range(1, len(min_armies)):
				if min_armies[i].n_armies > min_army:
					stop_point = i
					break
			min_armies = min_armies[:stop_point]
			min_vertex_numbers = sorted(min_armies, key=lambda x: x.id())
			territory = min_vertex_numbers[0]

		
		agent_action['placement'] = (territory, self._armies)
		return agent_action
