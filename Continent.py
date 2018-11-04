from Player import *
import View.Colors as colors

class Continent:
    def __init__(self, bonus, territories, color=None):
        self._bonus = bonus
        self._territories = territories
        self._owner = None
        self._color = color if color!=None else colors.random_color() # for gui purpose
    

    def color(self):
        return self._color

    def bonus(self):
        return self._bonus
        
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