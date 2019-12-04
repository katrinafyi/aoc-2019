from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
# import math
# from statistics import mean

INPUT = 'day04_input.txt'

# import numpy as np 
# import scipy as sp

def parse(lines):
    return tuple(map(int, (lines.split('-'))))
    
@lru_cache(maxsize=None)
def is_valid(num):
    num_str = str(num)
    # numbers must be not decreasing
    if any(int(num_str[i+1]) < int(num_str[i]) for i in range(len(num_str)-1)):
        return False
    # some number must be present at least twice
    if not any(v >= 2 for v in count_freq(num_str).values()):
        return False
    return True

def solve_1(data):
    valid = 0
    for x in range(data[0], data[1]+1):
        #print(x)
        if is_valid(x): valid += 1
    return valid

def solve_2(data):
    valid = 0
    for x in range(data[0], data[1]+1):
        #print(x)
        num_str = str(x)
        if is_valid(x) and any(v == 2 for v in count_freq(num_str).values()): 
            valid += 1
    return valid

if __name__ == "__main__":
    print('sol 1:', solve_1(parse('248345-746315')))
    print()
    print('sol 2:', solve_2(parse('248345-746315')))