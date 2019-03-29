import math
from display import *

def magnitude(vector):
    return sum(k**2 for k in vector)**.5

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    mag = magnitude(vector)
    vector[:] =  [ k/mag for k in vector]
    return vector

#Return the dot porduct of a . b
def dot_product(a, b):
    return [a[k] * b[k] for k in range(3)]

def cross_prod(a, b):
    return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):
    p0 = polygons[i]
    p1 = polygons[i+ 1]
    p2 = polygons[i + 2]
    a = [x1 - x0 for x1,x0 in zip(p1, p0)]
    b = [x2 - x0 for x2,x0 in zip(p2, p0)]
    return cross_pod(a, b)
def minus(a,b):
    return [k-v for k,v in zip(a,b)]
