
class Agent:
	def __init__(self, name):
		self.name = name

	def _init_placement(continents):
		# Among not-owned continents, choose the one with the max bonus, and put the armies
		# in a possible (not_owned) territory
		territory = None
		max_bonus = -1
		max_cont = None
		for cont in continents:
			if cont.owner != None:
				continue
			if max_bonus < cont.bonus():
				max_bonus = cont.bonus()
				max_cont = cont
		for t in max_cont.territories():
			if t.owner is None:
				territory = t
				break

		return territory
		
	def place_armies(self): # to be overriden
		return {} 

	def attack(self): # to be overriden
		return {}