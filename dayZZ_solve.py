from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
# import math
# from statistics import mean

DAY = '00'

# import numpy as np 
# import scipy as sp

def parse(file):
    pass

def solve_1(data):
    pass 

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(f'day{DAY}_input.txt') as f:
        print('sol 1:', solve_1(parse(f)))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f)))