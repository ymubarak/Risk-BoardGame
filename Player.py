

CONQUER_BONUS = 2

class Player:
    def __init__(self, pid):
        self._territories = []
        self._armies = 0
        self._id = pid


    def add_territory(self, territory):
        from Territory import Territory
        if not isinstance(territory, Territory):
            raise TypeError
        self._territories.append(territory)
        territory.owner = self
    
    def remove_territory(self, territory):
        from Territory import Territory
        if not isinstance(territory, Territory):
            raise TypeError
        self._territories.remove(territory)
        territory.owner = None
    

    def id(self):
        return self._id
    
    @property
    def armies(self):
        return self._armies
    
    @armies.setter
    def armies(self, armies):
        if not isinstance(armies, int):
            raise TypeError
        self._armies = 0 if armies<0 else armies


    def has_territory(self, t):
        return t in self._territories


    def conquer(self, attacker, attacked, placement):
        assert attacker in self._territories
        assert attacked in attacker.attackables()
        
        attacker.n_armies -= attacked.n_armies + placement
        attacked.n_armies = placement
        self._armies += CONQUER_BONUS
        attacked.owner.remove_territory(attacked)
        self.add_territory(attacked)