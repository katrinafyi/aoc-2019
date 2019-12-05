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
    index = 0
    is_position_mode = True
    while index < len(data):
        #print(index, data[index])

        m3, m2, m1, op = split_opcode(data[index])

        if op == 99: 
            print('HALT')
            break
        elif op in (1,2): # 1 or 2
            a = data[index+1]
            if m1 == 0: a = data[a]
            b = data[index+2]
            if m2 == 0: b = data[b]
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
            x = data[index+1]
            if m1 == 0: x = data[x]
            print('PROGRAM OUPUT:', x)
            index += 2
        elif op == 5: # jump if true
            x = data[index+1]
            if m1 == 0: x = data[x]
            if x != 0:
                index = data[index+2]
                if m2 == 0:
                    index = data[index]
            else:
                index += 3
        elif op == 6: # jump if false
            x = data[index+1]
            if m1 == 0: x = data[x]
            if x == 0:
                index = data[index+2]
                if m2 == 0:
                    index = data[index]
            else:
                index += 3
        elif op == 7: # less than
            a = data[index+1]
            if m1 == 0: a = data[a]
            b = data[index+2]
            if m2 == 0: b = data[b]
            out_pos = data[index+3]

            data[out_pos] = int(a < b)
            index += 4
        elif op == 8: # equals
            a = data[index+1]
            if m1 == 0: a = data[a]
            b = data[index+2]
            if m2 == 0: b = data[b]
            out_pos = data[index+3]

            data[out_pos] = int(a == b)
            index += 4
        else: 
            print('UNKNOWN OPCODE:', op)

    return data[0]

def solve_1(data):
    run_prog(1, data)

def solve_2(data):
    run_prog(5, data)

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))