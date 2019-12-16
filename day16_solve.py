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
def pattern2(n, shift=0):
    print('making transition (sub)matrix')
    mat = scipy.sparse.dok_matrix((n-shift, n-shift))
    base = [0, 1, 0, -1]
    for row in range(shift, n):
        if row % 100 == 0: print('row', row)
        this_base_len = (row+1) * len(base)
        start = row
        for col in range(start, n):
            val = base[(col+1) % this_base_len // (row+1)]
            if val:
                mat[row-shift, col-shift] = val
        # for col in range(start, n):
        #     this_index = (col+1) % this_base_len // (row+1)
        #     if base[this_index]: mat[row, col] = base[this_index]
        #     # print((row, col), base[this_index], end=' ')
        #     pass
    # mat = scipy.sparse.lil_matrix((n, n))
    # print('done dok construction')
    return mat.tocsr()

def apply_pattern_old(vec, n):
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

def apply_pattern(vec, full_len, shift=0):
    y = {}
    suffix = {}

    for i in range(full_len-1, shift-1, -1):
        if i + 1 < full_len:
            suffix[i] = suffix[i+1] + vec[i]
        else:
            suffix[i] = vec[i]

    for i in range(full_len-1, shift-1, -1):
        # print(i)
        # print(x)
        # print(y)
        if i + 2*(i+1) >= full_len:
            y[i] = suffix[i]
            if i+i+1 < full_len: 
                y[i] -= suffix[2*i+1]
        else:
            assert shift == 0 # should not be hit in part 2.
            # print(i, 'manual') 
            y[i] = apply_pattern_old(vec, i)
    
    for i, val in y.items():
        y[i] = abs(val) % 10
    return y

def solve_1(data):
    x = data
    print('len', len(x))
    for iteration in range(100):
        # print(iteration)
        # y = pattern(len(x)) @ x
        # y = np.mod(np.abs(y), 10)
        x = apply_pattern(x, len(data), 0)
        # print(y)
        # print(x)
        # for i, row in enumerate(x - y):
        #     if row:
        #         print(i, row, )
        #         # print(i, pattern(len(x))[i,:])
        # x = np.array(x)
        # print(x.values())
        # input('pause at' + str(iteration))

    # dictionary order is NOT guaranteed!
    return [x[i] for i in range(8)]
    # return tuple(x.values())[:8]

def solve_2(data):
    # print(data)

    shift = int(''.join(map(str, data[:7])))

    full_len = len(data) * 10000
    data_dict = {}
    for i in range(shift, full_len):
        data_dict[i] = data[i % len(data)]

    # print(pattern2(full_len, shift))
    x = data_dict
    print('data len:', len(data), 'full_len:', full_len, 'after len:', len(x), 'fraction:', len(x) / full_len)

    for iteration in range(100):
        print(iteration, end=' ', flush=1)
        x = apply_pattern(x, full_len, shift)
        # print(x.values())
        # input()
    print()
    return [x[i+shift] for i in range(8)]
    # pattern = 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))