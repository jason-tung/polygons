from draw import *
from alt_parser import *
from matrix import *
import math
from white_display import *

screen = new_screen()
color = [0, 0, 0]
edges = []
polygons = []
transform = new_matrix()

parse_file('altscript', edges, polygons, transform, screen, color)
