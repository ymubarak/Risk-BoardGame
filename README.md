# Risk-BoardGame

## Overview
This is an implementation of a simple environment simulator that generates instances of a search problem, runs agent programs, and evaluates their performance according to a simple performance measure. The search problem we will use is a simplified and abstract version of the board game RISK. Before reading on to the rest of the docs, be sure you understand the rules of the full version of the game. The following discussion will discuss how
the rules of the simplified, abstract game differ from the full version of the game.

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
* GUI mode
* Non-GUI mode (*For analysis*)

In a terminal or command window, navigate to the top-level project directory `Risk-BoardGame/` and run one of the following commands:

1. For **GUI mode**
```bash
python Run.py graph_specs_file_number 
```
where `graph_specs_file_number` is an indicator of the specification file of the game graph. Sample specifciaitoin are proivded in folder `input`. For example, to rune the game with graph specs *1*:
```bash
python Run.py 1 
```

2. To run the game with **Non-GUI mode**, add the `-nogui` argument:
```bash
python Run.py graph_specs_file_number -nogui
```

### GUI mode GamePlay

![splashscreen](https://github.com/youssef-ahmed/Risk-BoardGame/blob/master/screenshots/gameplay_1.png)

Choose player:  

![splashscreen](https://github.com/youssef-ahmed/Risk-BoardGame/blob/master/screenshots/gameplay_2.png)

Gameplay:  

![splashscreen](https://github.com/youssef-ahmed/Risk-BoardGame/blob/master/screenshots/gameplay_4.png)  

* Box 1  
  Player turn phase ( placement or Attack)
* Box 2  
  Player info: number, type, bonus armies, and percentage of land acquisition
* Box 1  
  Territory info: color (of its contenot), red circle contains number of armies, ID (white label)
* Box 3  
  Continent color-> bonus

### Non-GUI mode  

![nogui](https://github.com/youssef-ahmed/Risk-BoardGame/blob/master/screenshots/nogui_1.PNG)
