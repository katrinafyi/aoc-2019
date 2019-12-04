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
    
def is_valid(num):
    num_str = str(num)
    adjacents = [i for i in range(len(num_str)-1) if num_str[i] == num_str[i+1]]
    #print(adjacents)
    adjacents = [i for i in adjacents if (i+2 >= len(num_str) or num_str[i+2] != num_str[i]) and (i < 1 or num_str[i-1] != num_str[i])]
    #print(adjacents)
    if not adjacents: return False 

    prev = num_str[0]
    for char in num_str:
        if (int(char) < int(prev)):
            return False 
        prev = char
    return True

def solve_1(data):
    valid = 0
    for x in range(data[0], data[1]+1):
        #print(x)
        if is_valid(x): valid +=1
    return valid

def solve_2(data):
    pass 

if __name__ == "__main__":
    print('sol 1:', solve_1(parse('248345-746315')))
    print()
    print('sol 2:', solve_2(parse('248345-746315')))