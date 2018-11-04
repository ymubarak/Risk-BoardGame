from GameHandler import *
from View.Game import Game

from Player import *
from Agents import Agent


file_path = "input/specification.txt"
handler = GameHandler(file_path)
g = Game(handler)
g.run()