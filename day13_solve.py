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

    def project_ball(pos, vel, board):
        def remove_blocks(positions):
            for p in positions:
                if board.get(p, 0) == 2:
                    board[p] = 0

        limit = -24
        t = 0
        while (pos).imag > limit:
            print(pos)
            lpos, rpos = tuple(x+pos for x in turns[vel])
            adj_pos = lpos, pos+vel, rpos

            diag = int(board[pos + vel] != 0)
            left, right = tuple(int(board[x+pos] != 0) for x in turns[vel])

            adj = (left, diag, right)
            if adj != (0, 0, 0):
                print('hit at', pos, adj)

            if adj == (0, 0, 0):
                pass
            elif adj == (0, 1, 0) or adj == (1, 0, 1) or adj == (1, 1, 1):
                vel = -vel 
                remove_blocks(adj_pos)
            elif adj[2] == 1:
                remove_blocks((adj_pos[2], ))
                vel = co.turn_left(vel)
            elif adj[0] == 1:
                remove_blocks((adj_pos[2], ))
                vel = co.turn_right(vel)
            if (pos+vel).imag > limit:
                break
            board[pos] = 0
            pos += vel
            board[pos] = 4
            t += 1
        print('projected to', t, pos)
        return pos, t

    # def recurse(b_pos, b_vel, p_pos, board):

    #     p_pos = (20-23j)
    #     b_pos = (19-21j)

    #     while any(x == 2 for x in board.values()):
    #         end_pos, steps = project_ball(b_pos, b_vel)
    


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
            b_pos = pos
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
            print('ball at', b_pos, 'vel', co.name_map.get(b_vel, 0))
            # if b_vel: print('velocity', co.name_map[b_vel])
            print('player at', p_pos)
        # print()
    print()
    print()
    print('ended')
    return a

from itertools import count
def test(p):
    displayed = 0
    for i in count():
        try:
            x = p.run_to_output()
            y = p.run_to_output()
            t = p.run_to_output()
        except IndexError:
            return True, p
        if None in (x, y, t): 
            break
        if x == -1 and y == 0:
            displayed = t
            continue
    return displayed, i

def filter_stupid(seq):
    i = 20
    for j in seq:
        i += j 
        if not 0 < i < 24:
            return False 
    return True

def copy_program(prog: IntCode):
    p = IntCode(prog.data.copy(), prog.inputs.copy())
    p.index = prog.index 
    p.relbase = prog.relbase 
    return p

from itertools import product
def solve_2(data):
    
    data[0] = 2

    q = deque()
    q.append(((), IntCode(defaultdict(int, enumerate(data)), deque())))
    while q:
        seq, prog = q.pop()
        print(seq)
        # print(len(seq))

        score, time = test(prog)
        if score is True:
            for tail in (-1, 0, 1):
                new_prog = copy_program(prog)
                new_prog.inputs.append(tail)
                q.append((seq + (tail, ), new_prog))
        elif score > 0:
            print('score', score)
            print('seq', seq)

    

if __name__ == "__main__":
    with open(INPUT) as f:
        # print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))