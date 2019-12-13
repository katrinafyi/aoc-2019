from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from itertools import *
from math import *
from typing import *

from intcode import *

# import math
# from statistics import mean

INPUT = 'day13_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return ints(','.join(lines))

def solve_1(data):
    p = IntCode.from_list(data)

    board = {}

    for i in count():
        x = p.run_to_output()
        y = p.run_to_output()
        t = p.run_to_output()
        if None in (x, y, t): break

        pos = (x,y)
        board[pos] = t

    chars = [' ', '#', '.', '=', 'o']
    for y in range(25):
        for x in range(40):
            c = board.get((x, y), 0)
            print(chars[c], end='')
        print()
    # print()
    # if b_vel: print('velocity', co.name_map[b_vel])
    return sum(x == 2 for x in board.values())

"""
0 is an empty tile. No game object appears in this tile.
1 is a wall tile. Walls are indestructible barriers.
2 is a block tile. Blocks can be broken by the ball.
3 is a horizontal paddle tile. The paddle is indestructible.
4 is a ball tile. The ball moves diagonally and bounces off objects.
"""
def solve_2(data):
    
    data[0] = 2

    p = IntCode.from_list(data)

    b_pos = None 
    p_pos = None 

    p.inputs.append(0)

    display = None
    for iteration in count():
        x = p.run_to_output() 
        y = p.run_to_output()
        t = p.run_to_output()
        if None in (x, y, t): break
        if x == -1 and y == 0:
            display = t
            continue 
        pos = (x,y)
        if t == 3:
            p_pos = pos
        elif t == 4:
            b_pos = pos

        if t in (3,4): 
            pass
            # print(iteration, x,y,t, 'player', p_pos, 'ball', b_pos)
        
        # do not send input during initial render of board.
        if iteration < 25 * 40: continue 
        
        if t == 4:
            p.inputs.append(sign(b_pos[0] - p_pos[0]))
    print('took', iteration, 'iterations')
    print('ended. displayed:', display)
    return display


if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))