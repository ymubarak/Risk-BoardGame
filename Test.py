from GameHandler import *
from View.Game import Game

from Player import *
from Agents import Agent
import time

def gui():
    file_path = "input/specification.txt"
    handler = GameHandler(file_path)
    g = Game(handler)
    g.run()


def no_gui():
    # test without gui
    file_path = "input/specification2.txt"
    handler = GameHandler(file_path)

    p1 = 'Greedy Agent'
    p2 = 'Greedy Agent'
    wait_time = 0.5
    handler.create_players(p1, p2)

    while(True):
        turn, gameover = handler.get_game_state()
        players = handler.players()
        if gameover:
            print("player {} wins".format((turn+1)%2 +1))
            print("gameover")
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
    gui()