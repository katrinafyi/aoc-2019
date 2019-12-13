from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from math import *
from typing import *

import os

from intcode import *

# import math
# from statistics import mean

INPUT = 'day13_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return ints(','.join(lines))

def solve_1(data):
    import coords as co

    data[0] = 2
    p = IntCode(defaultdict(int, enumerate(data)), [None])

    b_pos = None 
    b_vel = co.SW
    p_pos = None

    board = defaultdict(int)

    turns = {
        co.NE: [co.N, co.E],
        co.SE: [co.E, co.S],
        co.SW: [co.S, co.W],
        co.NW: [co.W, co.N]
    }

    def project_ball(pos, vel):
        limit = -23
        while (pos).imag > limit:
            diag = int(board[pos + vel] != 0)
            left, right = tuple(int(board[x+pos] != 0) for x in turns[vel])

            adj = (left, right, diag)
            if adj != (0, 0, 0):
                print('hit at', pos, adj)
            if adj == (0, 0, 0):
                pass
            elif adj == (0, 1, 0) or adj == (1, 0, 1) or adj == (1, 1, 1):
                vel = -vel 
            elif adj[2] == 1:
                vel = co.turn_left(vel)
            elif adj[0] == 1:
                vel = co.turn_right(vel)
            if (pos+vel).imag > limit:
                break
            pos += vel
        print('ended at', pos)




    a = 0
    from itertools import count
    for i in count():
        p.inputs[0] = 0
        x = p.run_to_output()
        y = p.run_to_output()
        t = p.run_to_output()
        if None in (x, y, t): break

        if x == -1 and y == 0:
            print('displaying:', t)
            continue
        pos = co.from_pos((x, y))
        board[pos] = t
        if t == 4:
            if b_pos is not None: 
                b_vel = pos - b_pos
            b_pos = pos
            if b_vel is not None:
                project_ball(b_pos, b_vel)
                input('wait')
        elif t == 3:
            p_pos = pos

        if t in (3,4):
            pass
            # print(i, t, pos)
        
        if t == 4: 
            chars = [' ', '#', '.', '=', 'o']
            for y in range(25):
                for x in range(40):
                    c = board.get(co.from_pos((x, y)), 0)
                    print(chars[c], end='')
                print()
            # print()
            print('ball at', b_pos)
            # if b_vel: print('velocity', co.name_map[b_vel])
            print('player at', p_pos)
        # print()
    print()
    print()
    print('ended')
    return a

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))