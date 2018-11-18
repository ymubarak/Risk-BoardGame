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

    def territories(self):
        return self._territories


    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, owner):
        if owner is not None and not isinstance(owner, Player):
            raise TypeError
        self._owner = owner
    
    def has_territory(self, t):
        return t in self._territories

    def reinforce_owner(self):
        if self._owner is not None:
            self._owner.armies += self._bonus 