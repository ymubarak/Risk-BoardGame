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
        state.armies = state.armies - attacked.n_armies
        state.opponent_armies = state.opponent_armies - attacked.n_armies
        state.player.conquer(attacker, attacked, state.placement//2)
        print("attakcer armies after attack:", attacker.n_armies)
        print("attakced armies after attack:", attacked.n_armies)

    def simulate_placement(self):
        # place armies
        ids = []
        for t in self.player._territories:
            ids.append(t.id())

        weights = {}
        w=0
        for c in self.continents:
            for t in c._territories:
                if t.id() not in ids:
                    w = 0
                    for nbr in t.neighbors():
                        if nbr.id() in ids:
                            w+=1
                    weights[t.id()] = w
        
        tid, w = sorted(weights.items(), key=lambda x: x[1])[-1]
        new_state = copy.deepcopy(self)
        candidates = []
        for c in self.continents:
            for t in c._territories:
                if t.id() == tid:
                    for nbr in t.neighbors():
                        if nbr.id() in ids:
                            candidates.append(nbr.id())
                    break
        
        best_candidate = None
        max_val = 0
        for t in new_state.player._territories:
            if t.id() in candidates:
                if t.n_armies > max_val:
                    best_candidate = t
                    max_val = t.n_armies

        # placement
        print("place", new_state.player.armies, "in territory", best_candidate.id())
        best_candidate.n_armies += new_state.player.armies
        new_state.armies += new_state.player.armies
        new_state.player.armies = 0
        return new_state

    def neighbors(self):
        _neighbors = []
        
        state = self.simulate_placement()
        # check attackability for state creation
        for t in state.player._territories:
            for attackble in t.attackables():
                print(t.id(), ">can attack>", attackble.id())
                # p_shallow_copy = copy.copy(self.parent)
                new_state = copy.deepcopy(state)
                new_state.parent = state
                self.simulate_attack(new_state, t.id(), attackble.id())
                _neighbors.append(new_state)
        print("State neighbors found: ", len(_neighbors))
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

