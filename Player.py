from Territory import *

class Player:

    def __init__(self):
        self._territories = []
        self._armies = 0
        self._conquer_bonus = 0


    def add_territory(self, territory):
        if not isinstance(territory, Territory):
            raise TypeError
        self._territories.append(territory)

    @property
    def armies(self):
        return self._armies
    
    @armies.setter
    def armies(self, armies):
        if not isinstance(armies, int):
            raise TypeError
        new_val = self._armies+armies
        self._armies = 0 if new_val<0 else new_val


    def conquer(self, attacker, attacked, placement):
        assert attacked in attacker.attackables()
        
        attacker.n_armies -= attacked.n_armies + placement
        attacked.n_armies = placement
        self._conquer_bonus += 2


    def reinforce(self):
        if self._conquer_bonus > 0:
            self._armies += self._conquer_bonus
            self._conquer_bonus = 0