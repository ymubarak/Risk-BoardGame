
class Agent:
	def __init__(self, name):
		self.name = name

	def place_armies(self): # to be overriden
		return {} 

	def attack(self): # to be overriden
		return {}