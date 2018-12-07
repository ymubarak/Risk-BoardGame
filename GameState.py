import copy

class GameState:
    def __init__(self, player, continents):
        self.parent = None
        self.player = player
        self.continents = continents
        self.f_value = 0
        self.attacker = None
        self.attacked = None
        self.placement = 0
        self.armies = 0
        self.opponent_armies = 0
            
        for c in self.continents:
            for t in c._territories:
                if t.owner.id() == player.id():
                    self.armies += t.n_armies
                else:
                    self.opponent_armies += t.n_armies

    def territories_ration_per_continent(self):
        ids = []
        for t in self.player._territories:
            ids.append(t.id())

        total = 0
        for c in self.continents:
            t_num = 0
            for t in c._territories:
                if t.id() in ids:
                    t_num += 1
            total += 1 - t_num/len(c._territories)
        return total

    def simulate_attack(self, state, attacker_id, attacked_id):
        attacker = None        
        attacked = None
        print("p: ",state.player.id())
        for t in state.player._territories:
            if t.id() == attacker_id:
                attacker = t
                print("attacker found", t.id())
                for t2 in attacker.attackables():
                    if t2.id() == attacked_id:
                        print("attacked found", t2.id())
                        attacked = t2
                        break

        state.attacker = attacker
        state.attacked = attacked
        state.placement = attacker.n_armies - attacked.n_armies
        # update total armies
        state.armies = self.armies - attacked.n_armies
        state.opponent_armies = self.opponent_armies - attacked.n_armies
        state.player.conquer(attacker, attacked, state.placement//2)
        print("attakcer after:", attacker.n_armies)
        print("attakced after:", attacked.n_armies)



    def neighbors(self):
        _neighbors = []
        for t in self.player._territories:
            for attackble in t.attackables():
                print(t.id(), ">>", attackble.id())
                p_shallow_copy = copy.copy(self.parent)
                new_state = copy.deepcopy(self)
                new_state.parent = self
                self.simulate_attack(new_state, t.id(), attackble.id())
                _neighbors.append(new_state)
        print("eded..... ", len(_neighbors))
        return _neighbors


    def __lt__(self, other):
        if other is not None and not isinstance(other, GameState):
            raise NotImplementedError("lt is not defined for type {}".format(type(other)))
        print(self.f_value, " <> ", other.f_value)
        return self.f_value < other.f_value

    def __eq__(self, other):
        if other is None:
            return self is None
        if not isinstance(other, GameState):
            raise NotImplementedError("equality is not defined for type {}".format(type(other)))
        x = set([t.id() for t in self.player._territories])
        y = set([t.id() for t in other.player._territories])
        return not (x-y)

    
    def __hash__(self):
       return hash(id(self))

    # for debugging purpose
    def print_state(self):
        space = "    "
        p = self.player
        print("Player{}".format(p.id()) )
        print("{}Armies: {}".format(space, p.armies))
        print("{}Lands:".format(space))
        for t in p._territories:
            print("{} tid: {}".format(space*2, t.id()))
            print("{}Armies: {}".format(space*3, t.n_armies))

