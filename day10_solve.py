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

@lru_cache(maxsize=None)
def angle(a, b):
    assert a != b
    
    dx, dy = tup_sub(b, a)
    if dx == 0: 
        dy //= abs(dy)
    elif dy == 0:
        dx //= abs(dx)
    else:
        g = math.gcd(dx, dy)
        dx, dy = dx // g, dy // g
    return (dx, dy)


def solve_1(data):
    m = Maxer()
    for centre in data:
        d = set(data)
        d.remove(centre)
        angles = set(map(lambda x: angle(centre, x), d))
        m.update(centre, len(angles))
    return m.get_max()

def solve_2(data):
    centre = solve_1(data)[0]

    def ell2(a,b):
        return sum(map(lambda x: x*x, tup_sub(a, b)))**0.5

    data.remove(centre)

    def angle_deviation(a):
        """ Computes angle of point a from the centre origin. 
        Positive means clockwise, angle of 0 is straight up.
        """
        a = (-90 + math.degrees(math.atan2(-a[1], -a[0])))
        return (a) % 360
    
    all_angles = sorted(map(
        lambda y: (angle_deviation(angle(centre, y)),ell2(centre, y), angle(centre, y), y)
    , data))
    
    
    cur_a2 = None
    q = deque(all_angles)
    i = 0 # number of vaporised asteroids
    while i < 200:
        x = q.popleft()
        if cur_a2 is None or cur_a2 != x[2]:
            cur_a2 = x[2]
            # vaporise this asteroid
            #print(i, x) 
            i += 1
        else:
            q.append(x)
    return x

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))