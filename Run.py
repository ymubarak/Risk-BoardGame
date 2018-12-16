from GameHandler import *
from View.Game import Game

from Player import *
from Agents import Agent
import time

def gui(file_path):
    # test with gui
    handler = GameHandler(file_path)
    g = Game(handler)
    g.run()


def no_gui(file_path):
    # test without gui
    handler = GameHandler(file_path)
    player_types =('Passive Agent', 'Agressive Agent', 'Pacifist Agent',
            'Greedy Agent', 'A-Star Agent', 'A-Star-real-time Agent')
    print("\n\nPlayer Types:")

    for i, p in enumerate(player_types):
        print("{}. {}".format(i+1, p))
    
    p1 = int(input("\nChoose pLayer 1: ")) -1
    p2 = int(input("Choose pLayer 2: ")) -1
    wait_time = 0.5
    handler.create_players(player_types[p1], player_types[p2])

    while(True):
        turn, gameover = handler.get_game_state()
        players = handler.players()
        if gameover:
            pid = (turn+1)%2 +1
            name =  player_types[p1] if pid == 1 else player_types[p2]
            print("Game Over")
            print("player {} ({}) wins".format(pid, name) )

            if p1 > 2:
                player1 = handler.players()[0]
                p = player1.calc_performance(1)
                print("Player 1 performance=", p)
            if p2 > 2:
                player2 = handler.players()[1]
                p = player2.calc_performance(1)
                print("Player 2 performance=", p)
            break

        # time.sleep(wait_time)
        agent_action = players[turn].place_armies()
        if agent_action.get('placement', ()):
            territory = agent_action['placement'][0]
            placed_armies = agent_action['placement'][1]
            print("player{}: {} armies in t{}".format(turn+1, placed_armies, territory.id()))
            territory.n_armies+= placed_armies
            players[turn].armies -= placed_armies
            if not players[turn].has_territory(territory):
                players[turn].add_territory(territory)
            

        
        phn = handler.change_phase()
        # time.sleep(wait_time)

        agent_action = players[turn].attack()
        if agent_action.get('attack', ()):
            attacker = agent_action['attack'][0]
            attacked = agent_action['attack'][1]
            placed_armies = agent_action['attack'][2]
            print("player{}: t{}:{} attacked t{}:{}".format(turn+1, attacker.id(), attacker.n_armies,
             attacked.id(), attacked.n_armies))
            players[turn].conquer(attacker, attacked, placed_armies)

        handler.switch_turn()
        _ , gameover = handler.get_game_state()
        if not gameover:
            handler.change_phase()


if __name__ == '__main__':
    import sys
    file_path = None
    if len(sys.argv) == 1:
        file_path = "input/specification1.txt"
        gui(file_path)
    elif len(sys.argv) == 2:
        file_path = "input/specification{}.txt".format(sys.argv[1])
        gui(file_path)
    elif len(sys.argv) == 3:
        file_path = "input/specification{}.txt".format(sys.argv[1])
        if sys.argv[2] == '-nogui':
            no_gui(file_path)
        else:
            print("Invalid 3rd argument: '{}'' ".format(sys.argv[2]))
    else:
        print("Too many number of arguments; {} entered while expected at max 3 !".format(len(sys.argv)))