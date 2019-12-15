from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from math import *
from typing import *
from itertools import *

from intcode import *
import coords as co

# import math
# from statistics import mean

INPUT = 'day15_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return ints(lines[0])

directions = {
    1: co.N,
    2: co.S,
    3: co.W,
    4: co.E,
}

rev_dir = {
    v:k for k, v in directions.items()
}

def solve_1(data):
    from copy import deepcopy
    p = IntCode.from_list(data)

    board = dict() 
    pos = co.ORIGIN
    oxygen = None

    q = deque() 
    # program in the queue is assumed to be at the given position.
    q.append(((), co.ORIGIN, p)) 
    seen = set()
    while q:
        seq, pos, p = q.pop()
        # print(seq, pos)
        if pos in seen: 
            continue 
        board[pos] = ' '
        seen.add(pos)

        original = p

        for value, dir in directions.items():
            new_seq = seq + (dir, )
            new_pos = pos + dir
            p = deepcopy(original)
            p.inputs.append(value)
            x = (p.run_to_output())
            # print('test:',value, '=', x)
            if x == 0: 
                board[new_pos] = '#'
                continue # hit wall. ignore.
            if x == 2: 
                board[new_pos] = ' '
                oxygen = new_pos
                print(new_seq, len(new_seq), oxygen)
                # return
            else:
                board[new_pos] = ' '
            q.append((new_seq, new_pos, p))
            # go back.
            # print('input:',rev_dir[-dir])
    print('done exporation using intcode')
    q = deque() 
    q.append((0, oxygen))
    seen = set()
    max_t = 0
    while q:
        t, pos = q.pop()
        if pos in seen: continue 
        max_t = max(t, max_t)
        seen.add(pos)
        if t % 10 == 0: print(t, pos)
        for dir in co.CARDINALS:
            if board[pos + dir] != '#':
                q.append((t+1, pos+dir))
    print(max_t)

        
    # print(board)


def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))