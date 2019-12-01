from util import * 
from collections import defaultdict, deque, namedtuple
# import math
# from statistics import mean

DAY = '01'

# import numpy as np 
# import scipy as sp

def fuel(m):
    return int(m / 3 ) - 2

def parse(file):
    for l in file:
        yield int(l.strip())

def solve_1(data):
    return sum(fuel(x) for x in data)

def fuel_recursive(m):
    f = 0
    while m > 0:
        this_f = fuel(m)
        if this_f <= 0: break
        
        f += this_f
        m = this_f
        #print(this_f)
    return f

def solve_2(data):
    return sum(fuel_recursive(x) for x in data)

if __name__ == "__main__":
    with open(f'day{DAY}_input.txt') as f:
        sol = solve_2(parse(f))
        print('solution:', sol)