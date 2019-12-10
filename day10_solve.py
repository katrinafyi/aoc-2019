from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
from typing import *
import sys

import fractions as frac

# import math
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

    m = Maxer() 
    for centre in data:
        groups = defaultdict(set)
        remaining = set(data)
        remaining.remove(centre)
        #print('testing centre of', centre)
        while remaining:
            other = remaining.pop()
            #print('  direction of', other)

            a = centre 
            b = other
            dx = b[0] - a[0]
            dy = b[1] - a[1]
            g = frac.gcd(dx, dy)
            dx //= g
            dy //= g
            groups[(dx,dy)].add(other)

            for other2 in tuple(remaining):
                if is_on_line(*centre, *other, *other2):
                    #print('   found on line:', other2)
                    groups[(dx,dy)].add(other2)
                    remaining.remove(other2)
        from pprint import pprint 
        #print(centre, (groups))
        m.update(centre, len(groups) + 1)
    print(m.get_max())
    

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))