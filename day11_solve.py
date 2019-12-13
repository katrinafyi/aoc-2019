from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from typing import *
from intcode import *
import sys
# import math
# from statistics import mean

INPUT = 'day11_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp
def parse(lines: List[str]):
    return map_int(''.join(lines).strip().split(','))

def run_painter(p: IntCode, board: dict, default_colour: int=0):
    pos = co.ORIGIN
    direction = co.N

    turns = (co.turn_left, co.turn_right)
    while True:
        # note .get avoids adding the last position to the dict if halts here.
        p.inputs.append(board.get(pos, default_colour))
        # first output is colour of this pos
        c = p.run_to_output()
        if c is None: break
        board[pos] = c

        # next output is direction.
        d = p.run_to_output()
        if d is None: break
        direction = turns[d](direction)

        pos += direction
    return board


import coords as co
def solve_1(data):
    # 0 is black, 1 is white
    board = {}

    p = IntCode(defaultdict(lambda: 0, enumerate(data)))
    
    board[co.ORIGIN] = 0
    run_painter(p, board)
    return len(board)

def solve_2(data):
    board = defaultdict(lambda: 0)

    p = IntCode(defaultdict(lambda: 0, enumerate(data)))
    
    board[co.ORIGIN] = 1
    run_painter(p, board)

    colours = [' ', '#']
    for y in range(0,8):
        for x in range(0, 50):
            print(colours[board[co.from_pos((x,y))]], end='')
        print()

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))