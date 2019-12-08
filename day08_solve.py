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

def solve_1(data):
    layers = []
    i = 0
    while i < len(data):
        x = ''
        for _ in range(25*6):
            x += data[i]
            i += 1
        layers.append(x)
    
    m = Maxer(is_max=False) 
    for l in layers:
        m.update(l, l.count('0'))
    l = (m.get_max())[0] 

    print(l.count('1') * l.count('2'))
    image = {(x,y): 2 for x in range(25) for y in range(6)}
    for l in reversed(layers):
        for i, char in enumerate(l):
            x = i % 25 
            y = i // 25
            assert y < 6
            if char == '2': 
                pass 
            else: 
                assert (x,y) in image
                image[(x,y)] = int(char)
    
    for y in range(6):
        for x in range(25):
            c = image[(x,y)]
            if c == 2:
                print('X', end='')
            elif c == 1:
                print('#', end='')
            elif c == 0:
                print(' ', end='')
            else:
                print(c, 'invalid colour')
                assert False
        print()





def solve_2(data):
    # 0 black,
    # 1 white
    # 2 transparent
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))