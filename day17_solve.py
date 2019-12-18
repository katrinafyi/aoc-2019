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

    pos = next(pos for pos in board if board[pos] == '^')
    hashes.add(pos)
    path = ''
    vel = co.N
    while True:
        if pos+vel in hashes:
            letter = ''
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
        path += letter + 'F'
    opath = path
        # print(letter, end='')
        # if letter in 'LR': print()

    letters = 'CBA'

    get_tail = lambda path: ''.join(takewhile(lambda c: c not in letters, dropwhile(lambda c: c in letters, path)))

    def compress_str(s):
        f_len = 0
        out = []
        for c in s:
            if c == 'F':
                f_len += 1
            else:
                if f_len:
                    out.append(str(f_len))
                    f_len = 0
                out.append(c)
        if f_len:
            out.append(str(f_len))
            f_len = 0
        return ','.join(out)

    @lru_cache(maxsize=None)
    def compress_segment(cpath, remaining):
        if remaining == 0: 
            return (not bool(cpath.strip(letters))) and len(compress_str(cpath)) <= 20, ()
        # print('trying to compress', cpath)
        for seg_len in range(1, len(cpath)):
            seg = get_tail(cpath)[:seg_len]
            path = cpath.replace(seg, letters[remaining-1])

            if len(compress_str(seg)) > 20: break

            status, segments = compress_segment(path, remaining-1)
            if status:
                return True, (seg, ) + segments
        return False, ()

    result, segments = compress_segment(opath, 3)
    print(result, segments)
    # print(repr(opath))

    print('#' * 20)
    for seg in segments:
        print(compress_str(seg))

    data = list(data)
    data[0] = 2
    p = IntCode.from_list(data)

    path = opath
    for letter, seg in zip(letters[::-1], segments):
        print(letter, seg)
        path = path.replace(seg, letter)

    print(opath)
    print(path)

    to_ascii = lambda string: [ord(x) for x in string]

    p.inputs.extend(to_ascii(compress_str(path) + '\n'))
    for seg in segments:
        print('inputtin', seg)
        p.inputs.extend(to_ascii(compress_str(seg) + '\n'))
    p.inputs.extend(to_ascii('n\n'))
    print([chr(x) for x in p.inputs])
    # print(list(board.keys())[-10:])
    print('last output:', p.run_to_halt()[-1])
    return

    i = 0
    while True:
        if i % (29 * 45) == 0: input(0)
        print(chr(p.run_to_output()), end='')
        i += 1
    return


    B = 'L'
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