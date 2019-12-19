from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from math import *
from typing import *
from itertools import *

from intcode import *

# import math
# from statistics import mean

DEBUG = '-v' in sys.argv
if DEBUG: sys.argv.remove('-v')
def dprint(*args, **kwargs): 
    if DEBUG: print(*args, **kwargs)

INPUT = 'day19_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return tuple(ints(lines[0]))

def test_pos(clean_p, x, y):
    p = clean_p.deepcopy()
    p.inputs = [x, y]
    return p.run_to_halt()[0] == 1

from fractions import Fraction

test_case = '''#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..'''

def solve_1(data):

    s = 0
    clean_p = IntCode.from_list(data)

    def square_fits(x, y):
        return test_pos(clean_p, x + 99, y) and test_pos(clean_p, x, y+99   )

    test = test_case.split('\n')

    xs = []
    for y in range(3999,4000):
    # for y in (len(test)-1, ):
        for x in range(2500,4000):
            # if x >= len(test[0]): break
            if test_pos(clean_p, x, y):
            # if test[y][x] != '.':
                print('#', end='')
                xs.append(x)
            else:
                print('.', end='')
        print() 
    
    y_shift = 3999
    size = 100

    # y_shift = len(test)-1
    # size = 10

    left_bound = xs[0]
    left_grad = Fraction(left_bound, y_shift)
    right_bound = xs[-1]
    right_grad =  Fraction(right_bound, y_shift)

    print(left_bound, right_bound)
    is_next = False
    for i in count(1):
        top = floor(right_grad * i )
        bottom = ceil(left_grad * i )
        if top - bottom >= size and bottom+size-1 <= floor(right_grad * (i-(size-1))):
            
            print(i, top, bottom)
            res = bottom-1, i-(size-1)-1
            print('res',res)
            break

    for shifts in ((0, 0), (0, size-1), (size-1, 0), (size-1, size-1)):
        print(shifts, test_pos(clean_p, shifts[0] + res[0], shifts[1] + res[1]))


    x,y = res
    print(res)
    print('sol?', 10000*x + y)
    return

    binary_search(lambda n: not square_fits(n, n), 4, 1)

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))