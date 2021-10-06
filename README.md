# Risk-BoardGame

## Overview

This is an implementation of a simple environment simulator that generates instances of a search problem, runs agent programs, and evaluates their performance according to a simple performance measure. The search problem we will use is a simplified and abstract version of the board game RISK. Before reading on to the rest of the docs, be sure you understand the rules of the full version of the game. The following discussion will discuss how
the rules of the simplified, abstract game differ from the full version of the game.

## Board Overview

In the abstract version of the game, the board is just an undirected graph, where each territory
(country) is a vertex, and a graph edge signies that territories have a common border (and thus
a country represented by one vertex can attack the country represented by the other vertex).
In addition, the graph is partitioned into several (connected) subgraphs, and each partition cell
represents a continent and has its respective bonus (received for holding all of it).
Your program should be able to read the graph specication from a le, in a format such as:
V 4 ; number of vertices
E 4 ; number of edges
(1 2) ; edges
(2 3)
(3 4)
(1 3)
P 2 ; number of partition cells
5 1 2 ; value of the 1st partition cell, and its members
3 3 4 ; value of the 2nd partition cell, and its members
It is easy to specify the RISK map in the board game, if so desired...

## Simplified Game Rules

This abstract version of the game makes it more general, but not necessarily more compli-
cated. The following is a list of simplications:

1. RISK is a multi-player game, but we will assume that only 2 players are in the game in the simplified version.

2. RISK has cards that can be cached in for armies - we will have no cards in our version. Instead  of  cards,  a  player  which  conquers  at  least  one  node  (territory),  receives  an additional bonus of 2 armies at the next turn.

3. In this initial exercise, the battles are deterministic. Denote A(v) the number of armies
in vertex v. Vertex v can attack vertex u only if there is an edge between these vertices, and A(v) - A(u) > 1. As a result of the battle, each opposing player loses A(u) armies, and the attacking player must move at least 1 army to u, but must leave at least 1 army in v.

4. Initial placement of armies is determined as part of the input, and not by the agent.

5. When getting the armies at the beginning of a turn, they must all be placed on the same
vertex.

6. For this initial exercise, the enemy is completely passive, i.e. it never attacks, and always
places all its additional armies on the vertex that has the fewest armies, breaking ties by
favoring the lowest-numbered vertex.

7. Initially, a turn will consist of: placing the bonus armies at the beginning of the turn, moving armies from one node to the other, and doing at most one attack (including moving armies into the captured territory). There will be no fortifying step, for simplicity.

8. Each player has at most one move, he can do with his troops, moving troops should be from one node to the other that belongs to the current player making the movement.

9. Each player has at most one attack, from one of his node to another node belongs to the enemy. the attack is successful, if it satisfied the above attack rules.

10. Each agent would make his attack according to heuristic, except for the human agent, as it would attack as he wants according to his heuristic.

## Objective

The goal of the game is to conquer the world in the smallest number of turns.

## Project Structure

```python
Risk-BoardGame
├── README.md #This File
├── requirements.txt # Python dependencies
├── input # Samples of Graph specification files
├── Agents # Search agents(Naive + Intelligent)
├── Media
    ├── sound
    └── images
└── Run.py # main file
```

## Requirments

This project requires **Python 3.x** and the following Python libraries installed:

- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Pygame](https://www.pygame.org/)
- [Networkx](https://networkx.github.io/)

## Run

The game has two modes:

- GUI mode
- Non-GUI mode (*Useful for analysis*)

In a terminal or command window, navigate to the top-level project directory `Risk-BoardGame/` and run one of the following commands:

1. For **GUI mode**

   ```bash
   python Run.py graph_specs_file_number
   ```

   where `graph_specs_file_number` is an indicator of the specification file of the game graph. Sample specifciaitoin are proivded in folder `input`. For   example, to rune the game with graph specs *1*:

   ```bash
   python Run.py 1
   ```

2. For **Non-GUI mode**, add the `-nogui` argument:

   ```bash
   python Run.py graph_specs_file_number -nogui
   ```

### Sample Runs

#### GUI mode GamePlay

![splashscreen](https://github.com/ymubarak/Risk-BoardGame/blob/master/screenshots/gameplay_1.png)

Choose player:

![choose player window](https://github.com/ymubarak/Risk-BoardGame/blob/master/screenshots/gameplay_2.png)

Main Window:

![in-game window](https://github.com/ymubarak/Risk-BoardGame/blob/master/screenshots/gameplay_4.png)

- Box 1

  Player turn phase ( placement or Attack)
- Box 2

  Player info: number, type, bonus armies, and percentage of land acquisition
- Box 1

  Territory info: color (of its contenot), red circle contains number of armies, ID (white label)
- Box 3
  Continent color-> bonus

Gameplay:

### Non-GUI mode

![nogui mode](https://github.com/ymubarak/Risk-BoardGame/blob/master/screenshots/nogui_1.PNG)
