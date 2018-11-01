from Player import *
from Territory import *
from Continent import *

turn = None
continents = []
players = []
graph = {}

def read_game(file_path):
    file = open(file_path, "r")
    try:
        line = next(file).strip()
        v = int(line.split(" ")[-1])
        
        # create graph map
        global graph
        graph = {}
        for i in range(1, v+1):
            graph[i] = Territory(i)
        
        # read edges
        line = next(file).strip()
        e = int(line.split(" ")[-1])
        for i in range(e):
            line = next(file)[1:-2] # skip parenthesis
            edge_pair = line.split(" ")
            t_from = int(edge_pair[0])
            t_to = int(edge_pair[1])
            graph[t_from].add_neighbor(graph[t_to])
        
        # read continents
        line = next(file).strip()
        p = int(line.split(" ")[-1])
        for i in range(p):
            arr = next(file).strip().split(" ")
            bonus = int(arr[0])
            territories = []
            for t_id in arr[1:]:
                territories.append(graph[int(t_id)])
            
            c = Continent(bonus, territories)
            continents.append(c)

    except StopIteration:
        pass
    
    init_game()


def init_game():
    global players, turn
    turn = 0
    players = [Player(), Player()]
    players[0].armies = 3
    players[1].armies = 3


def play()
    while True:
        switch_turn()


def switch_turn():
    global turn
    turn = 1 if turn==0 else 0
    # phase 1
    players[turn].reinforce()
    for c in continents:
        if players[turn] == c:
            c.reinforce_owner()

    # phase 2
    # if turn == 0 (human turn)
        # wait for gui interaction/decission
        # - place armies
        # - attack ==> choose new placement
    # else:
        # TODO: choose an agent to play 
    

# for debugging purpose
def print_state():
    space = "    "
    for i, p in enumerate(players):
        print("Player{}".format(i+1))
        print("{}Armies: {}".format(space, p.armies))
        print("{}Lands:".format(space))
        for t in p._territories:
            print("{} tid: {}".format(space*2, t._id))
            print("{}Armies: {}".format(space*3, t.n_armies))