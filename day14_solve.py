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

def compute_ore_needed(fuel, by_result):
    required = defaultdict(int)
    required['FUEL'] = fuel
    while True:
        # print(required)
        mats_needed =set (x for x in required if required[x] > 0 and x != 'ORE')
        if not mats_needed: break

        m = mats_needed.pop()
        p_ing, p_amount = by_result[m]
        p_mul = ceil(required[m] // p_amount)
        # print('need for', m, need)
        for mat, amount in p_ing.items():
            required[mat] += amount * p_mul
        required[m] -= p_amount * p_mul
    return required['ORE']

    if any(x < 0 for x in required.values()):
        # print(fuel, 'had leftover')
        # continue
        pass
    return required['ORE']

def solve_1(data):
    from copy import deepcopy 
    original = deepcopy(data)
    
    def to_dict(mat_list):
        return {m.name: m.amount for m in mat_list}

    recipes: List[Tuple[List[Mat], Mat]] = (data)
    # recipes are a pair (ingredients, quantity) where ingredients is a dict
    # keyed by material with values of number required.
    by_result = {result.name: (to_dict(input), result.amount) for input, result in recipes}


    # expand all non-ORE ingredients into the producing recipes and maintain
    # perfect ratio. merges all recipes into one 'mega recipe' from ORE to FUEL
    mega_ing, mega_amount = deepcopy(by_result['FUEL'])
    while any(m != 'ORE' for m in mega_ing.keys()):
        # print(mega_ing, mega_amount)
        target = next(m for m in mega_ing.keys() if m != 'ORE')
        # print(target, by_result[target])
        p_ing, p_amount = (by_result[target])
        l = (lcm(p_amount, mega_ing[target]))

        p_mul = l // p_amount 
        m_mul = l // mega_ing[target]

        for k in mega_ing:
            mega_ing[k] *= m_mul
        for new_ing in p_ing:
            if new_ing not in mega_ing: mega_ing[new_ing] = 0
            mega_ing[new_ing] += p_ing[new_ing] * p_mul
        mega_ing[target] -= p_amount * p_mul
        assert mega_ing[target] == 0
        del mega_ing[target]
        mega_amount *= m_mul
        # print(mega_ing, mega_amount)
        # return
    trillion = 1000000000000
    print(mega_ing, mega_amount)
    mega_ore = mega_ing['ORE']

    from fractions import Fraction 

    ratio = Fraction(mega_ore, mega_amount)
    print(ratio)

    mega_ore, mega_amount = ratio.numerator, ratio.denominator
    
    clean_fuel = mega_amount * (trillion // mega_ore)
    remaining_ore = trillion % mega_ore

    

    print('remaining ore:', remaining_ore)

    def test_fuel(fuel):
        required = defaultdict(int)
        required['FUEL'] = fuel
        while True:
            # print(required)
            mats_needed =set (x for x in required if required[x] > 0 and x != 'ORE')
            if not mats_needed: break

            m = mats_needed.pop()
            need, produced = find_recipe(Mat(required[m], m))
            # print('need for', m, need)
            for x in need:
                required[x.name] += x.amount
            required[produced.name] -= produced.amount

        if any(x < 0 for x in required.values()):
            # print(fuel, 'had leftover')
            # continue
            pass
        ore = required['ORE']
        return ore <= remaining_ore
    
    nasty_fuel = binary_search(test_fuel)

    print('>> clean multiple fuel: ', clean_fuel)
    print('>> binary searched fuel: ', nasty_fuel)
    return clean_fuel + nasty_fuel

    

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))