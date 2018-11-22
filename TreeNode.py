from Territory import *

class TreeNode:
    def __init__(self, t, g_value_, h_value_, parent = None):
        self._t = t
        self._g_value = g_value_
        self._h_value = h_value_
        self._parent = parent

    @property
    def t():
        return self._t
    
    @property
    def g_value(self):
        return self._g_value

    @g_value.setter
    def g_value(self, new_val):
        self._g_value = new_val
        
    @property
    def h_value(self):
        return self._h_value
    
    @h_value.setter
    def h_value(self, new_val):
        self._h_value = new_val

    @property
    def parent(self):
        return self._parent
    

    def total_value(self):
        return self._g_value + self._h_value
        
    def __lt__(self, other):
        return self.total_value() < other.total_value()