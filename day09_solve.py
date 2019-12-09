from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from typing import List, Tuple, Dict
import sys
# import math
from statistics import mean

INPUT = 'day09_input.txt' if len(sys.argv) == 1 else sys.argv[1]

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
                Param must not be in immediate mode.
                """
                x = data[self.index+num]
                # relative is 2, normal position mode is 0.
                assert modes[num-1] != 1
                if modes[num-1] == 2:
                    return x+self.relbase
                return x

            def get_param(num): 
                """
                Gets the num-th operation parameter, starting from 1, 
                and applying the modes.
                """
                # immediate mode is 1, other modes use indirection.
                if modes[num-1] == 1:
                    return data[self.index+num]
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

def solve_1(data):
    d = defaultdict(lambda: 0, enumerate(data))
    prog = IntCode(d, [1])
    while True:
        y = prog.run_to_output()
        if y is None: break
        x = y
        print(y)
    return x

def solve_2(data):
    d = defaultdict(lambda: 0, enumerate(data))
    prog = IntCode(d, [2])
    x = prog.run_to_output()
    return x

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))