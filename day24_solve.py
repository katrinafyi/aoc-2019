from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from math import *
from typing import *
from itertools import *

# from intcode import *

# import math
# from statistics import mean

DEBUG = '-v' in sys.argv
if DEBUG: sys.argv.remove('-v')
def dprint(*args, **kwargs): 
    if DEBUG: print(*args, **kwargs)

INPUT = 'day24_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

import coords as co

def parse(lines: List[str]):
    board = dict()
    for y, row in enumerate(lines):
        row = row.rstrip()
        for x, char in enumerate(row):
            board[co.from_pos(x, y)] = char == '#'
    return board

def solve_1(data):
    board = data

    seen = set()



    bug_levels = defaultdict(set)
    bug_levels[0] = frozenset(x for x in board if board[x])
    centre = co.from_pos(2,2)

    def max_norm(x):
        return max(map(abs, co.to_pos(x)))

    for iteration in range(3):

        min_level = min(bug_levels.keys())
        max_level = max(bug_levels.keys())
        if bug_levels[min_level]:
            bug_levels[min_level-1] = set()
        if bug_levels[max_level]:
            bug_levels[max_level+1] = set()

        print(iteration, len(bug_levels))
        new_bugs = defaultdict(set)
        for level, bugs in bug_levels.items():
            this_new_bugs = set()
            for y in range(5):
                for x in range(5):
                    if (x,y) == (2,2): continue 

                    pos = co.from_pos(x,y)
                    adj_bugs = 0 
                    for adj in co.adjacents(pos):
                        a_pos = co.to_pos(adj)
                        if adj == centre:
                            direction = pos - centre
                            start = pos + direction + co.turn_left(direction)*2
                            direction = co.turn_right(direction)
                            for _i in range(5):
                                if (start + _i*direction) in bug_levels.get(level-1, ()):
                                    adj_bugs += 1
                                # print(pos, start + _i*direction)
                        elif min(a_pos) == -1 or max(a_pos) == 5:
                            if a_pos[0] == -1:
                                outer_pos = co.from_pos(1,2)
                            elif a_pos[0] == 5:
                                outer_pos = co.from_pos(3,2)
                            elif a_pos[1] == -1:
                                outer_pos = co.from_pos(2,1)
                            elif a_pos[1] == 5:
                                outer_pos = co.from_pos(2,3)
                            else: 
                                assert 0, a_pos
                            print(a_pos, co.to_pos(outer_pos))
                            if outer_pos in bug_levels.get(level+1, ()):
                                adj_bugs += 1
                        elif adj in bugs:
                            adj_bugs += 1 


                    has_bug = pos in bugs
                    if has_bug and adj_bugs != 1:
                        # bug dies at pos
                        # new_board[pos] = False
                        pass
                    elif (not has_bug) and adj_bugs in (1,2):
                        this_new_bugs.add(pos)
                    elif has_bug:
                        this_new_bugs.add(pos)
            new_bugs[level] = this_new_bugs

        count = 0
        print('iteration', iteration)
        for level, bugs in sorted(bug_levels.items()):
            print('level', level)
            for y in range(5):
                for x in range(5):
                    has_bug = co.from_pos(x,y) in bugs
                    if has_bug: count += 1
                    print('.#'[has_bug], end='')
                print()
            print()

        bug_levels = new_bugs

        # bug_positions = frozenset(new_bugs)
        # if bug_positions in seen: 
        #     print('repeated')
        #     print(bug_positions)
        #     break
        # seen.add(bug_positions)
        # bugs = new_bugs

    
    print(count)


            

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))