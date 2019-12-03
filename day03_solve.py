from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass

# import math
# from statistics import mean

INPUT = 'day03_input.txt'

# import numpy as np 
# import scipy as sp

def parse(lines):
    wires = [] # array of wires. each wire is an array of steps defining that wire.
    for line in lines:
        steps = [] # array of steps. each step is a tuple (letter, length)
        for step in line.strip().split(','):
            steps.append((step[0], int(step[1:])))
        wires.append(steps)
    return wires

STEPS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def compute_intersections(wires):
    num_wires = len(wires)

    # mapping of position to array. value array contains length to reach that 
    # point for each wire. 
    grid = defaultdict(lambda: [None]*num_wires)
    #print(wires)
    for i, wire in enumerate(wires):
        #print(i)
        pos = (0,0)
        grid[pos][i] = 0
        wire_len = 1
        for step in wire:
            #print(step)
            d = STEPS[step[0]]
            for _ in range(step[1]):
                pos = tup_add(pos, d)
                if grid[pos][i] is None:
                    grid[pos][i] = wire_len
                wire_len += 1
                #print(pos)
    return [(pos, val) for pos, val in grid.items()
        if val[0] is not None and val[1] is not None and pos != (0,0)]

def solve_1(data):
    intersctions = compute_intersections(data)
    f = lambda x: manhattan((0,0), x[0])
    intersctions.sort(key=f)
    return intersctions[0], f(intersctions[0])

def solve_2(data):
    intersctions = compute_intersections(data)
    f = lambda x: sum(x[1])
    intersctions.sort(key=f)
    return intersctions[0], f(intersctions[0])

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))