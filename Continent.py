from Player import *

class Continent:
    def __init__(self, bonus, territories, color="green"):
        self._bonus = bonus
        self._territories = territories
        self._owner = None
        self.color = color # for gui purpose
    

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, owner):
        if not isinstance(owner, Player):
            raise TypeError
        self._owner = owner

    def reinforce_owner():
        if self._owner is not None:
            self._owner.armies += self.bonus 