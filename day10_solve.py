from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
from typing import *
import sys

import fractions as frac
from pprint import pprint

import math
# from statistics import mean

INPUT = 'day10_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    asteroids = set()
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char == '#':
                asteroids.add((x,y))
    return asteroids

def lcm(x, y):
    return x * y // frac.gcd(x, y)



    

def solve_1(data):
    max_y = max(pos[1] for pos in data)
    min_y = min(pos[1] for pos in data)
    max_x = max(pos[0] for pos in data)
    min_x = min(pos[0] for pos in data)

    from itertools import combinations

    def is_on_line(x1, y1, x2, y2, x3, y3):
        return (x2 - x1) * (y3 - y1) == (y2 - y1) * (x3 - x1)

    def grad(a, b):
        a = centre 
        b = other
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        g = frac.gcd(dx, dy)
        dx //= g
        dy //= g
        return (dx, dy)

    def ell2(a, b):
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

    m = Maxer() 

    for centre in data:

        def f(other):
            angle =( math.degrees(math.atan2(other[1] - centre[1], other[0] - centre[0])))
            if angle < 0: angle += 360
            return (angle, ell2(centre, other), other)

        centre = (22, 25)
        d = set(data)
        d.remove(centre)
        x = lmap(f, d)
        x.sort()
        pprint(x)
        print(x[199])
        
        break
        m.update(centre, len(angles))
    print(m.get_max())
    

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))