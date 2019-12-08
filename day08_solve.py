from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass
from typing import *
import sys
# import math
# from statistics import mean

INPUT = 'day08_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return ''.join(lines)

WIDTH = 25 
HEIGHT = 6

def solve_1(data):
    layers = chunks(data, WIDTH * HEIGHT)
    
    m = Maxer(is_max=False) 
    for l in layers:
        m.update(l, l.count('0'))
    l = (m.get_max())[0] 

    return (l.count('1') * l.count('2'))

def solve_2(data):
    layers = chunks(data, WIDTH * HEIGHT)

    image = {}
    # first layer is at the top and overrides lower layers.
    for l in reversed(layers):
        for i, char in enumerate(l):
            x = i % WIDTH 
            y = i // WIDTH
            assert 0 <= y < HEIGHT
            if char == '2': 
                pass 
            else: 
                image[(x,y)] = int(char)
    
    chars = {
        # 2 is transparent, 1 is white, 0 is black.
        2: 'X', 1: 'o', 0: ' '
    }
    for y in range(HEIGHT):
        for x in range(WIDTH):
            c = image[(x,y)]
            print(chars[c], end='')
        print()
    return None

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))