import heapq

class InformedSearch:
    def __init__(self, initial_state, controller, limit=0):
        self.initial_state = initial_state
        self.controller = controller
        self._graph_size = len(self.controller.graph())
        self.initial_state = initial_state
        self.g_function = lambda x: 0
        self.h_function = lambda x: 0
        self.limit = limit

    def set_heuristic(self, h=None):
        if h!=None:
            self.h_function = h
    
    def set_cost(self, g=None):
        if g!=None:
            self.g_function = g
        

    def f_function(self, state):
       return self.g_function(state) + self.h_function(state)
    

    def goal_test(self, state):
        return self._graph_size == len(state.player._territories)

    def get_search_result(self):
        last_state = self.serach()
        print("last state: ")
        last_state.print_state()
        if last_state.parent == None:   #no possible move
            return None

        while last_state.parent.parent != None:
            last_state = last_state.parent
            print("go up parent")

        print("attacker returned", last_state.attacker.id())
        return last_state.attacker.id(), last_state.attacked.id(), last_state.placement


    def serach(self):
        print("in search")
        self.initial_state.f_value = self.f_function(self.initial_state)
        self.frontier = [self.initial_state]
        self.explored = set()
        while self.frontier:
            heapq.heapify(self.frontier)
            state = heapq.heappop(self.frontier)
            self.explored.add(state)

            print("frontier_size:", len(self.frontier))
            if self.goal_test(state):
                return state

            print("player", state.player.id())
            print("state:>........")
            state.print_state()

            for neighbor in state.neighbors():
                print("expand neighbor")
                if self.limit > 0 and self.g_function(neighbor) > limit: # limit on depth
                    continue
                if not (neighbor in (set(self.frontier) | self.explored)):
                    neighbor.f_value = self.f_function(neighbor)
                    self.frontier.append(neighbor)
                elif neighbor in Set(self.frontier): # decrease key
                    print("try to decrease")
                    new_value = self.f_function(neighbor)
                    if new_value < neighbor.f_value:
                        neighbor.f_value = new_value
                else:
                    print("explored")

        # search failed 
        print("failed:")
        return min(self.explored)

