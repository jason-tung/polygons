from display import *
from draw import *
from gif_parser import *
from matrix import *
import math

screen = new_screen()
color = [0, 255, 0]
edges = []
polygons = []
transform = new_matrix()

parse_file('gifbase', edges, polygons, transform, screen, color)