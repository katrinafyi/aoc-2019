from util import * 

import sys
from collections import defaultdict, deque, namedtuple
# from dataclasses import dataclass, field
from math import *
from typing import *
from itertools import *

# from intcode import *

# import math
# from statistics import mean

DEBUG = '-v' in sys.argv
if DEBUG: sys.argv.remove('-v')
def dprint(*args, **kwargs): 
    if DEBUG: print(*args, **kwargs)

INPUT = 'day18_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

import string
import coords as co

def parse(lines: List[str]):
    board = dict()
    tup = []
    for y, row in enumerate(lines):
        row = row.strip()
        for x, char in enumerate(row):
            board[co.from_pos((x,y))] = char
        tup.append(tuple(row))
    return board

def csign(c):
    return complex(sign(c.real), sign(c.imag))

def solve_1(data):
    board = data

    all_keys = set(v for k, v in board.items() if v in string.ascii_lowercase)
    print(all_keys)

    start = next(k for k, v in board.items() if v == '@')
    at_symbol = start
    sys.setrecursionlimit(50000)

    pos = start
    q = deque()
    aug_board = dict()
    # position, length, keys_needed
    q.append((pos, 0, frozenset()))
    while q:
        pos, l, keys_needed = q.popleft()
        if pos in aug_board: continue 
        aug_board[pos] = (l, keys_needed)

        for adj in co.adjacents(pos):
            this_key = keys_needed
            if board[adj] == '#':
                continue 
            elif board[adj] in string.ascii_uppercase:
                this_key = keys_needed | {board[adj]}
            q.append((adj, l+1, this_key))
    key_dict = {k:(board[k],)+ v for k, v in aug_board.items() if board[k] in string.ascii_lowercase}
    print(aug_board)
    print(key_dict)
    # return

    distances = dict()

    @lru_cache(maxsize=None)
    def bfs_min_path(start, end, keys):
        # if csign(start-at_symbol) == -csign(end-at_symbol):
        #     # print('opt')
        #     return key_dict[start][1] + key_dict[end][1]

        q = deque()
        seen = set()
        q.append((start, 0))
        path_len = None
        while q:
            pos, l = q.popleft()
            if pos == end: 
                path_len = l
                break
            if pos in seen: continue 
            seen.add(pos)
            distances[frozenset((start, pos))] = l

            for adj in co.adjacents(pos):
                if board[adj] == '#':
                    continue 
                elif board[adj] in string.ascii_uppercase and board[adj] not in keys: 
                    continue
                q.append((adj, l+1))
        distances[frozenset((start, end))] = path_len
        return path_len


    @lru_cache(maxsize=None)
    def recurse(pos, keys: frozenset):
        # print('keys', keys)
        if len(keys) == len(all_keys):
            return 0

        min_path = float('inf')

        open_goals = set(k for k, v in key_dict.items() if len(v[2] - keys) == 0 and v[0].upper() not in keys)
        same_quadr = set(x for x in open_goals if csign(x - at_symbol) == csign(pos - at_symbol))
        if same_quadr:
            open_goals = same_quadr
        if not open_goals:
            print('no available open goals D:')
            return 0
        # print(open_goals)
        # return
        for next_goal in open_goals:
            if len(keys) <= 15:
                print('next', len(keys), 'goal is', next_goal, 'of', len(open_goals))
            # print('trying to get to', next_goal, 'for', board[next_goal])
            
            path_len = bfs_min_path(pos, next_goal, keys)
            
            assert path_len is not None
            # return path_len + recurse(next_goal, keys | {board[next_goal].upper()})
            min_path = min(path_len + recurse(next_goal, keys | {board[next_goal].upper()}), min_path)
        return min_path

    print('xd')
    print('sol?', recurse(start, frozenset()))
    print('done')

    # print(board)
    pass 

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))