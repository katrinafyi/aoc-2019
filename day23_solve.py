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

INPUT = 'day23_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return tuple(ints(lines[0]))

def solve_1(data):
    computers = [IntCode.from_list(data) for i in range(50)]

    for i in range(50):
        computers[i].inputs.append(i)
        # print(computers[i].run_to_input())

    nat = None
    idle = set()
    sent = set()
    while 1:
        if len(idle) == len(computers):
            if nat[1] in sent:
                print('repeated nat', nat)
                return
            sent.add(nat[1])
            computers[0].inputs.extend(nat)
        for i, c in enumerate(computers):
            # print(i)
            if not c.inputs:
                c.inputs.append(-1)
                idle.add(i)
            elif i in idle:
                idle.remove(i)
            for dst, x, y in chunks(c.run_to_input(), 3):
                if dst == 255:
                    nat = (x,y)
                    continue
                computers[dst].inputs.extend((x, y))


def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))