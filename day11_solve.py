from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from typing import *
import sys
# import math
# from statistics import mean

INPUT = 'day11_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp
def parse(lines: List[str]):
    return map_int(''.join(lines).strip().split(','))

def split_opcode(num):
    op = num % 100 
    return digits(num // 100, 3) + (op, )

@dataclass
class IntCode:
    data: list 
    inputs: list = field(default_factory=list)
    index: int = 0 
    relbase: int = 0

    def run_to_output(self):
        data = self.data
        while self.index < len(data):
            #print(index, data[index])

            m3, m2, m1, op = split_opcode(data[self.index])
            modes = m1, m2, m3

            def get_pos(num):
                """
                Gets the position referred to by the num-th parameter. 
                """
                m = modes[num-1]
                if m == 1: 
                    return self.index + num # immediate mode
                
                x = data[self.index+num]
                # relative is 2, normal position mode is 0.
                if m == 2: 
                    return x + self.relbase # relative mode
                elif m == 0: 
                    return x # position mode
                assert False

            def get_param(num): 
                """
                Gets the num-th operation parameter, starting from 1, 
                and applying the modes.
                """
                # immediate mode is 1, other modes use indirection.
                return data[get_pos(num)]

            if op == 99: 
                #print('HALT')
                return None
            elif op in (1,2): # 1 or 2
                a, b = get_param(1), get_param(2)
                out_pos = get_pos(3)
                
                #print(out_pos, out_pos % 4)
                if op == 1:
                    data[out_pos] = a + b
                else:
                    data[out_pos] = a * b
            
                self.index += 4
            elif op== 3: # input
                #print('waiting for input')
                data[get_pos(1)] = self.inputs.pop(0)
                #print('got input', data[data[index+1]])
                self.index += 2
            elif op == 4:
                x = get_param(1)
                #print('PROGRAM OUPUT:', x)
                #print('output', x)
                #print('got after output', (yield x))
                self.index += 2
                return x
            elif op == 5: # jump if true
                x = get_param(1)
                if x != 0:
                    self.index = get_param(2)
                else:
                    self.index += 3
            elif op == 6: # jump if false
                x = get_param(1)
                if x == 0:
                    self.index = get_param(2)
                else:
                    self.index += 3
            elif op == 7: # less than
                a, b = get_param(1), get_param(2) 
                out_pos = get_pos(3)

                data[out_pos] = int(a < b)
                self.index += 4
            elif op == 8: # equals
                a, b = get_param(1), get_param(2) 
                out_pos = get_pos(3)

                data[out_pos] = int(a == b)
                self.index += 4
            elif op == 9:
                x = get_param(1)
                self.relbase += x
                self.index += 2
            else: 
                print('UNKNOWN OPCODE:', op)
    
    def run_to_halt(self):
        out = []
        while True: 
            x = self.run_to_output()
            if x is None:
                break 
            out.append(x)
        return out

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