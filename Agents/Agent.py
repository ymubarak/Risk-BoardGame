

class Agent:
	def __init__(self, name):
		self.name = name

	def play(self): # tempalte method
		self.place_armies()
		self.attack()

	def place_armies(self): # to be overriden
		pass 

	def attack(self): # to be overriden
		pass