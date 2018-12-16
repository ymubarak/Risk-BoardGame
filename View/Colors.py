import random

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark = (21, 19, 21)
bluey = (2, 1, 28)

pallette = [(0, 0, 117), (19, 214, 194), (58, 0, 117), (255, 225, 25)]
last_color = -1

def to_rgb(hex_value):
	r = int(hex_value[1:3], 16)
	b = int(hex_value[3:5], 16)
	g = int(hex_value[5:], 16)
	return (r, g, b)

def to_hex(rgb):
	return '#%02x%02x%02x' % rgb

def random_color():
	r = random.randint(0,255)
	g = random.randint(0,255)
	b = random.randint(0,255)
	return (r, g, b)


def pick_pallette_color():
	global last_color
	last_color +=1
	return pallette[last_color]