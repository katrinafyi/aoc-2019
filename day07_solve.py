from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
import sys
# import math
from statistics import mean

INPUT = 'day07_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines):
    return map_int(lines[0].strip().split(','))

def split_opcode(num):
    op = num % 100 
    return digits(num // 100, 3) + (op, )


class Program:
    def __init__(self):
        self.index = 0

    def run_to_output(self):

        data = self.data 
        inputs = self.inputs

        out = None
        index = self.index
        while index < len(data):
            self.index = index
            #print(index, data[index])

            m3, m2, m1, op = split_opcode(data[index])

            modes = (m1, m2, m3)

            # get the num-th operation parameter, starting from 1, and applying the
            # mode.
            def get_param(num): 
                x = data[index+num]
                # immediate mode is 1, indirect mode is 0.
                if modes[num-1] == 1:
                    return x
                assert x >= 0
                return data[x]

            if op == 99: 
                #print('HALT')
                return None
            elif op in (1,2): # 1 or 2
                a, b = get_param(1), get_param(2)
                out_pos = data[index+3]
                
                #print(out_pos, out_pos % 4)
                if op == 1:
                    data[out_pos] = a + b
                else:
                    data[out_pos] = a * b
            
                index += 4
            elif op== 3: # input
                data[data[index+1]] = inputs.pop(0)
                index += 2
            elif op == 4:
                x = get_param(1)
                #print('PROGRAM OUPUT:', x)
                index += 2
                self.index = index
                return x
            elif op == 5: # jump if true
                x = get_param(1)
                if x != 0:
                    index = get_param(2)
                else:
                    index += 3
            elif op == 6: # jump if false
                x = get_param(1)
                if x == 0:
                    index = get_param(2)
                else:
                    index += 3
            elif op == 7: # less than
                a, b = get_param(1), get_param(2) 
                out_pos = data[index+3]

                data[out_pos] = int(a < b)
                index += 4
            elif op == 8: # equals
                a, b = get_param(1), get_param(2) 
                out_pos = data[index+3]

                data[out_pos] = int(a == b)
                index += 4
            else: 
                print('UNKNOWN OPCODE:', op)
            self.index = index

        return None

def solve_1(data):

    from itertools import permutations

    m = 0
    for perm in permutations((0, 1, 2, 3, 4)):
        x = 0
        i = 0

        for p in perm:
            prog = Program()
            prog.data = list(data)
            prog.inputs = [perm[i], x]
            x = prog.run_to_output()
            i += 1
        if x > m:
            m = x
    return m

def solve_2(data):
    from itertools import permutations

    m = 0
    for perm in permutations((5,6,7,8,9)):
        datas = [list(data) for _ in range(5)]
        inputs = [[perm[_]] for _ in range(5)]

        amplifiers = [Program() for i in range(5)]
        for i, a in enumerate(amplifiers):
            a.data = datas[i] 
            a.inputs = inputs[i]


        x = 0
        run = 1
        while run:
            for i, amp in enumerate(amplifiers):
                inputs[i].append(x)
                o = amp.run_to_output()
                if o is None: 
                    run = 0
                    break
                x = o
        print(perm, x)
        if x > m:
            m = x
    return  m
    #return run_prog(5, data)

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))