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
# import scipy as sp

def parse(lines: List[str]):
    return tuple(map(int, lines[0]))

@lru_cache()
def pattern(n):
    base = [0, 1, 0, -1]
    repeats = ceil(n / 4)
    stack = []
    for row in range(n):
        row_base = np.repeat(base, row+1)
        # print(row_base)
        this_row = tuple(islice(cycle(row_base), 1, 1+n))
        assert len(this_row) == n
        stack.append(this_row)
    print('done pattern')
    return np.vstack(stack)

def solve_1(data):
    print(data)

    data *= 10000
    vec = np.array(data)
    print(pattern(len(data)))
    x = vec
    input('wait ')
    for i in range(100):
        print(i)
        # print(x)
        x = np.mod(np.abs(pattern(len(data)) @ x.T), 10)
        # print(x)
        # input()
    print(x)
    print(tuple(x)[:8])

    # pattern = 


def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))