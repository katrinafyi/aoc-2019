from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
# import math
# from statistics import mean

INPUT = 'dayXX_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines):
    pass

def solve_1(data):
    pass 

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))