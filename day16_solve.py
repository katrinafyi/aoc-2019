from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from math import *
from typing import *
from itertools import *

# from intcode import *

# import math
# from statistics import mean

DEBUG = '-v' in sys.argv
if DEBUG: sys.argv.remove('-v')
def dprint(*args, **kwargs): 
    if DEBUG: print(*args, **kwargs)

INPUT = 'day16_input.txt' if len(sys.argv) == 1 else sys.argv[1]

import numpy as np 
import scipy as sp
import scipy.sparse

def parse(lines: List[str]):
    return tuple(map(int, lines[0]))

@lru_cache()
def pattern(n):
    # I was trying to be clever. This cost me about 10 minutes.
    base = [0, 1, 0, -1]
    repeats = ceil(n / 4)
    stack = []
    for row in range(n):
        row_base = np.repeat(base, row+1)
        # print(row_base)
        this_row = tuple(islice(cycle(row_base), 1, 1+n))
        assert len(this_row) == n
        stack.append(this_row)
    # print('done pattern')
    return np.vstack(stack)

@lru_cache()
def pattern2(n):
    mat_rows = []

    base = [0, 1, 0, -1]
    for row in range(n):
        if row % 100 == 0: print(row)
        this_base_len = (row+1) * len(base)
        start = row
        mat_rows.append([base[(col+1) % this_base_len // (row+1)] for col in range(start, n)])
        # for col in range(start, n):
        #     this_index = (col+1) % this_base_len // (row+1)
        #     if base[this_index]: mat[row, col] = base[this_index]
        #     # print((row, col), base[this_index], end=' ')
        #     pass
    # mat = scipy.sparse.lil_matrix((n, n))
    print('done dok construction')
    return scipy.sparse.csr_matrix(mat_rows)

def apply_pattern(vec, n):
    out = 0
    start = n
    period = 4 * (n+1)
    for i in range(start, len(vec), period):
        for j in range(n+1):
            if i+j >= len(vec): break
            out += vec[i+j]
    for i in range(start + period // 2, len(vec), period):
        for j in range(n+1):
            if i+j >= len(vec): break
            out -= vec[i+j]
    return out

def solve_1(data):
    print(data)
    shift = int(''.join(map(str, data[:7])))

    data *= 10000
    full_len = len(data)
    data_dict = {}
    for i, val in enumerate(data[shift:]):
        data_dict[shift+i] = val

    x = data_dict
    print(len(x))
    y = {}

    suffix = {}    
    # IMPORTANT: y and x only store items AFTER shift.
    for iteration in range(100):
        print(iteration)
        y = {}

        for i in range(full_len-1, shift-1, -1):
            if i + 1 < full_len:
                suffix[i] = suffix[i+1] + x[i]
            else:
                suffix[i] = x[i]

        for i in range(full_len-1, shift-1, -1):
            # print(i)
            # print(x)
            # print(y)
            if i + 2*(i+1) >= full_len:
                y[i] = suffix[i]
                if i+i+1 < full_len: 
                    y[i] -= suffix[2*i+1]
            else:
                print(i, 'manual')
                y[i] = apply_pattern(x, i)
        
        for i, val in y.items():
            x[i] = abs(y[i]) % 10
        # print(i, x)
        # for i, val in enumerate(correct - x):
        #     if val:
        #         print(i, pattern(len(x))[i,:])
        # input()
    print(list(x.values())[:8])
    # pattern = 


def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))