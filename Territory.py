from Player import *

class Territory:
    def __init__(self, t_id):
        self._id = t_id
        self._owner = None
        self._armies = 0
        self._neighbors = []


    @property
    def n_armies(self):
        return self._armies
    
    @n_armies.setter
    def n_armies(self, n_armies):
        if not isinstance(n_armies, int):
            raise TypeError
        new_val = self._armies+n_armies
        self._armies = 0 if new_val<0 else new_val

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, owner):
        if not isinstance(owner, Player):
            raise TypeError
        self._owner = owner

    def add_neighbor(self, neighbor):
        if not isinstance(neighbor, Territory):
            raise TypeError
        self._neighbors.append(neighbor)

    @property
    def neighbors():
        self._neighbors

    def attackables(self):
        attackables = []
        for nb in self._neighbors:
            if self._armies - nb.n_armies > 1:
                attackables.append(nb)

        return attackables
