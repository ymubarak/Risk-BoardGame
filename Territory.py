
class Territory:
    def __init__(self, t_id):
        self._id = t_id
        self._owner = None
        self._armies = 0
        self._neighbors = []


    def id(self):
        return self._id


    @property
    def n_armies(self):
        return self._armies
    
    @n_armies.setter
    def n_armies(self, n_armies):
        if not isinstance(n_armies, int):
            raise TypeError
        self._armies = 0 if n_armies<0 else n_armies

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, owner):
        from Player import Player
        if owner is not None and not isinstance(owner, Player):
            raise TypeError("Territory Owner must be a Player object or None")
        self._owner = owner

    def add_neighbor(self, neighbor):
        if not isinstance(neighbor, Territory):
            raise TypeError
        self._neighbors.append(neighbor)


    def neighbors(self):
        return self._neighbors

    def attackables(self):
        attackables = []
        for nb in self._neighbors:
            if (nb.n_armies >0 and
             nb.owner is not self._owner and self._armies - nb.n_armies > 1):
                attackables.append(nb)

        return attackables
