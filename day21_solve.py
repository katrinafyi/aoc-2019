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

INPUT = 'day21_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return ints(lines[0])

def a_to_s(a):
    return ''.join(map(chr, a))


def solve_1(data):
    # print(data)
    p = IntCode.from_list(data)
    # print(a_to_s(p.run_to_input()))
    springcode = '''OR A T
AND D T
NOT T T
AND A T
OR C T
OR B T
AND A T
NOT T J
AND J T
OR D T
AND E T
OR T J
RUN
'''
    springcode = '''NOT A J
OR B T
OR E T
NOT T T
OR T J

AND D J
RUN
'''
    springcode = '''OR B J
OR E J
OR C T
OR E T
OR F T
AND J T
AND A T
NOT T J
AND D J
RUN
'''

    for c in springcode: 
        p.inputs.append(ord(c))
    o = p.run_to_halt()
    print(a_to_s(o[:-1]))
    print(o[-1])



def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))