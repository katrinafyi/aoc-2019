from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
import sys
# import math
from statistics import mean

INPUT = 'day05_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines):
    return map_int(lines[0].strip().split(','))

def split_opcode(num):
    onum = num
    out = [0]*4
    out[-1] = num % 100
    num //= 100

    for i in range(3):
        out[-2-i] = num % 10;
        num //= 10
    print(onum, out)
    return out


def run_prog(input_value, data):
    data = list(data)

    out = None
    index = 0
    while index < len(data):
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
            return data[x]

        if op == 99: 
            print('HALT')
            break
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
            data[data[index+1]] = input_value
            index += 2
        elif op == 4:
            x = get_param(1)
            print('PROGRAM OUPUT:', x)
            out = x
            index += 2
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

    return out

def solve_1(data):
    return run_prog(1, data)

def solve_2(data):
    return run_prog(5, data)

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))