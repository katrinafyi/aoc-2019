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

INPUT = 'day14_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

@dataclass(frozen=1)
class Mat:
    amount: int 
    name: str

def parse_mat(mat_str):
    x = mat_str.split(" ")
    return Mat(int(x[0]), x[1])

def parse(lines: List[str]):
    out = []
    for l in lines:
        left, right = l.strip().split(' => ')
        left = left.split(', ')
        left = lmap(parse_mat, left)
        right = parse_mat(right)
        out.append((left, right))
    return out

def solve_1(data):
    from copy import deepcopy 
    original = deepcopy(data)

    recipes = (data)
    def find_recipe(goal: Mat):
        if goal.amount == 0: return ()
        out = []
        for input, output in recipes:
            if output.name == goal.name:
                repeats = ceil(goal.amount / output.amount)
                for m in input:
                    out.append(Mat(m.amount * repeats, m.name))
                return out, Mat(repeats * output.amount, output.name)
        assert 0

    by_result = {result: input for input, result in recipes}
    next_mat = deque()
    next_mat.append(Mat(1, 'FUEL'))
    while True:
        result = next_mat.popleft()
        if result == 'ORE'
        inputs = by_result[result]
        us = result.amount
        for i in inputs:
            us = lcm(us, i.amount)


            print()
        print(result, input)

    seen = set()
    for fuel in range(100000, 200000):
        required = defaultdict(int)
        prev_ore = 0
        required['FUEL'] = fuel
        while True:
            # print(required)
            mats_needed =set (x for x in required if required[x] > 0)
            if 'ORE' in mats_needed: mats_needed.remove('ORE')

            if not mats_needed: break

            m = mats_needed.pop()
            need, produced = find_recipe(Mat(required[m], m))
            # print('need for', m, need)
            for x in need:
                required[x.name] += x.amount
            required[produced.name] -= produced.amount

        if any(x < 0 for x in required.values()):
            print(fuel, 'had leftover')
            continue
        this = required['ORE'] - prev_ore
        print(fuel, '-th fuel took', this)
        if this in seen:
            print('seen!')
        seen.add(this)
        prev_ore = required['ORE']


        

    

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))