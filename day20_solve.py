from util import * 

import sys
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from math import *
from typing import *
from itertools import *

# from intcode import *

import string

# import math
# from statistics import mean

DEBUG = '-v' in sys.argv
if DEBUG: sys.argv.remove('-v')
def dprint(*args, **kwargs): 
    if DEBUG: print(*args, **kwargs)

INPUT = 'day20_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

import coords as co 

def parse(lines: List[str]):
    board = dict() 
    letter_positions = dict() 
    donut_rows = []
    inner_top_left = None
    for y, row in enumerate(lines):
        row: str = row
        if '#' in row:
            donut_rows.append(y)
        if ' ' in row and y > 2 and inner_top_left is None:
            inner_top_left = (y, row.index(' ', 2))

        for x, char in enumerate(row):
            if char == '#' or char == '.':
                board[co.from_pos(x,y)] = char 
            elif char in string.ascii_uppercase:
                letter_positions[co.from_pos(x,y)] = char

    # print(board)

    portal_pairs = defaultdict(set)

    for pos, letter in letter_positions.items():
        for shift in co.CARDINALS:
            if pos + shift in letter_positions:
                if shift in (co.N, co.W):
                    portal = letter_positions[shift+pos] + letter 
                else: 
                    portal = letter + letter_positions[shift+pos]  

                portal_pairs[portal].add(frozenset((pos, pos+shift)))
    
    # print(portal_pairs)


    def find_pos_nearest_maze(pair):
        for p in pair:
            for a in co.adjacents(p):
                if a in board and board[a] not in string.ascii_uppercase:
                    return a
        assert 0

    portals = dict() 
    for code, pairs in portal_pairs.items():
        if code == 'AA':
            AA = find_pos_nearest_maze(next(iter(pairs)))
            continue
        elif code == 'ZZ':
            ZZ = find_pos_nearest_maze(next(iter(pairs)))
            continue
        in_pos, out_pos = tuple(pairs)

        # print(code, in_pos, out_pos)
        near_pos_in = find_pos_nearest_maze(in_pos)
        near_pos_out = find_pos_nearest_maze(out_pos)
        portals[near_pos_in] = near_pos_out
        portals[near_pos_out] = near_pos_in        
        
    # print(portals, AA, ZZ)
    # print('a', lines[90][73])
    return board, portals, AA, ZZ
            

def compute_keys_dict(board, start):
    board = board.copy()
    q = deque()
    aug_board = {}
    parents = {start: None}
    # position, length, keys_needed
    q.append((start, 0, frozenset()))
    while q:
        pos, l, keys_needed = q.popleft()
        if pos in aug_board: continue 
        aug_board[pos] = (l, keys_needed)

        for adj in co.adjacents(pos):
            this_key = keys_needed
            if board[adj] == '#':
                continue 
            q.append((adj, l+1, this_key))
    return {k:(board[k],)+ v for k, v in aug_board.items() if board[k] in string.ascii_lowercase}

def solve_1(data):
    board, portals, AA, ZZ = data 

    portal_positions = set(portals)
    
    @lru_cache(maxsize=None)
    def compute_reachable_portals(start):
        q = deque() 
        seen = set() 
        q.append((start, 0))
        reachable_portals = dict()
        while q: 
            pos, l = q.popleft() 
            if pos in seen: continue 
            if pos in portal_positions or pos == ZZ:
                reachable_portals[pos] = l
            seen.add(pos) 
            for adj in co.adjacents(pos):
                if board.get(adj, None) != '.':
                    continue 
                q.append((adj, l+1))
        return reachable_portals

    print(compute_reachable_portals(AA))

    edges = []
    for p in tuple(portals.keys()) + (AA, ):
        for other, l in compute_reachable_portals(p).items():
            edges.append((p, other, {'weight':l}))

    for p_in, p_out in portals.items():
        edges.append((p_in, p_out, {'weight':1}))

    import networkx as nx 

    g = nx.Graph()
    
    g.add_edges_from(edges)
    # print('nodes', g.nodes)
    # print(g.edges)
    print('start is', AA)
    print(AA in g.nodes, ZZ in g.nodes)

    # print(list(g.neighbors(AA)))
    # print(list(g.neighbors(ZZ)))
    # print(list(g.neighbors((73-90j))))

    print(nx.algorithms.shortest_path_length(g, AA, ZZ, weight='weight'))
    return
    

    sys.setrecursionlimit(3000)
    @lru_cache(maxsize=None)
    def recurse(pos, seen: frozenset):
        if pos == ZZ: return 0
        # print(pos, seen)
        seen |= {pos}

        min_len = float('inf')
        for portal_pos, l in compute_reachable_portals(pos).items():
            if portals[portal_pos] in seen: continue
            min_len = min(l + 1 + recurse(portals[portal_pos], seen | {portal_pos}), min_len)
        return min_len

    print(recurse(AA, frozenset()))

    

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))