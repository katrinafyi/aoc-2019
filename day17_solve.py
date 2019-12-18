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

INPUT = 'day17_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return tuple(ints(lines[0]))

def longestRepeatedSubstring(str): 
  
    n = len(str) 
    LCSRe = [[0 for x in range(n + 1)]  
                for y in range(n + 1)] 
  
    res = "" # To store result 
    res_length = 0 # To store length of result 
  
    # building table in bottom-up manner 
    index = 0
    for i in range(1, n + 1): 
        for j in range(i + 1, n + 1): 
              
            # (j-i) > LCSRe[i-1][j-1] to remove 
            # overlapping 
            if (str[i - 1] == str[j - 1] and
                LCSRe[i - 1][j - 1] < (j - i)): 
                LCSRe[i][j] = LCSRe[i - 1][j - 1] + 1
  
                # updating maximum length of the 
                # substring and updating the finishing 
                # index of the suffix 
                if (LCSRe[i][j] > res_length): 
                    res_length = LCSRe[i][j] 
                    index = max(i, index) 
                  
            else: 
                LCSRe[i][j] = 0
  
    # If we have non-empty result, then insert  
    # all characters from first character to  
    # last character of string 
    if (res_length > 0): 
        for i in range(index - res_length + 1, 
                                    index + 1): 
            res = res + str[i - 1] 
  
    return res 

import coords as co
def solve_1(data):
    p = IntCode.from_list(data)

    output = p.run_to_halt()

    chars = lmap(chr, output)
    big_str = ''.join(chars)
    print(big_str)

    board = {}
    for y, row in enumerate(big_str.split('\n')):
        for x, c in enumerate(row):
            board[co.from_pos((x,y))] = c
    hashes = set(pos for pos in board if board[pos] == '#')

    isections = []
    for pos in hashes:
        isection = True
        for adj in co.adjacents(pos):
            if adj not in hashes: 
                isection = False 
                break
        if isection:
            isections.append(pos)
    
    print(sum(abs(x.imag) * abs(x.real) for x in isections))

    # part 2
    data = list(data)
    data[0] = 2
    p = IntCode.from_list(data)

    pos = next(pos for pos in board if board[pos] == '^')
    hashes.add(pos)
    path = ''
    vel = co.N
    while True:
        if pos+vel in hashes:
            letter = 'F'
            pos += vel
        else:
            vel = co.turn_left(vel)
            if pos+vel in hashes:
                letter = 'L'
                pos += vel
            else:
                vel = co.turn_right(vel)
                vel = co.turn_right(vel)
                if pos+vel in hashes:
                    letter = 'R'
                    pos += vel
                else: break
        path += letter
    opath = path
        # print(letter, end='')
        # if letter in 'LR': print()

    from collections import Counter
    A = B = C = 'fjev wiovj fweionvjio'


    B = 'L'
    A = 'FFFLFFFFFFFFFFFRFF'
    # C = 'F'
    the_char = 'B'
    A_prefix = 1
    A_suffix = None
    while A_suffix or A_prefix:
        path = opath
        # C = 'FFF'*3
        path = path.replace(A, 'A')
        path = path.replace(B, 'B')
        # path = path.replace(C, 'C')
        if 'B' not in path: break
        A_prefix = None 
        A_suffix = None
        for i, c in enumerate(path):
            if i+1 < len(path) and path[i+1] == the_char:
                if A_prefix is None:
                    A_prefix = c
                elif A_prefix != c:
                    A_prefix = False 
            
            if i > 0 and path[i-1] == the_char:
                if A_suffix is None:
                    A_suffix = c
                elif A_suffix != c:
                    A_suffix = False 
        if A_prefix: 
            B = A_prefix + B
        if A_suffix: 
            B = B + A_suffix
        
        print(the_char, 'is prefixed by', A_prefix, 'suffix', A_suffix)
    print(B)
    # print(path)
    # s = path
    # for n in range(1, len(s)):
    #     m = Maxer()
    #     for shift in range(n):
    #         substr_counter = Counter()
    #         new = [s[i: i+n] for i in range(shift, len(s) - n, n)]
    #         new = [x for x in new if not any(char in 'ABC' for char in x)]
    #         substr_counter.update(new)
    #         mc = substr_counter.most_common(1)
    #         if mc and mc[0]:
    #             m.update(*mc[0])
    #     k, v = (m.get_max())
    #     if v is not None and v > 1:
    #         print(k, v, len(k) * v)
    # print(big_str)
    print(len(path))


    s = path
    f_start = None
    print(s, 'L' in s, 'R' in s)
    for i in range(len(s)):
        if s[i] == "F":
            if f_start is None:
                f_start = i 
        elif s[i] != 'F' and f_start is not None:
            # print('F', i-f_start)
            f_start = None
    print('encoded len', len(s) * 2)
    # print(opath)

            
        
        # phrase, count = substr_counter.most_common(1)[0]
        # if count == 1:      # early out for trivial cases
        #     break
        # print 'Size: %3d:  Occurrences: %3d  Phrase: %r' % (n, count, phrase)

    # LRS = longestRepeatedSubstring

    # print('original', path)
    # # print(LRS(path))
    # A = (LRS(LRS(path)))

    # path = path.replace(A, 'A')
    # B = 'FRFFFRFFFLFFFFFFFFFFFRFFFFFLFFFFFFFFFFF'
    # path = path.replace(B, 'B')
    # print(path)
    # print(LRS(path))

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))