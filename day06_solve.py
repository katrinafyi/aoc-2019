from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
import sys
# import math
# from statistics import mean

INPUT = 'day06_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines):
    return [tuple(l.strip().split(')')) for l in lines]


def solve_1(data):
    orbits = set(data )



    cum_orbits = defaultdict(lambda: 0)
    while True:
        left_planets = set(x[0] for x in orbits)
        right_planets = set(x[1] for x in orbits)

        tails = (right_planets - left_planets)
        if not tails: break

        to_remove = set()
        for o in orbits:
            if o[1] in tails:
                cum_orbits[o[0]] += 1 + cum_orbits[o[1]]
                to_remove.add(o)

        orbits -= to_remove
    print(cum_orbits)
    print(sum(cum_orbits.values()))

    
        

def solve_2(data):
    orbits = set(data)

    src = [x for x in orbits if x[1] == 'YOU'][0][0]
    dest = [x for x in orbits if x[1] == 'SAN'][0][0]

    seen = set()
    q = deque()
    pos = None 
    q.append((src, 0))
    while pos != dest:
        pos, dist = q.popleft()
        seen.add(pos)
        for x in orbits:
            if x[0] == pos:
                if x[1] not in seen:
                    q.append((x[1], dist+1))
            elif x[1] == pos:
                if x[0] not in seen:
                    q.append((x[0], dist+1))

    print(pos, dist, q)

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))