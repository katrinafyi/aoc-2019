#!/usr/bin/env python3.8
from util import * 

import sys
print(sys.version)
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
# from math import *
from typing import *
from itertools import *

# from blist import blist

# from intcode import *

# import math
# from statistics import mean

DEBUG = '-v' in sys.argv
if DEBUG: sys.argv.remove('-v')
def dprint(*args, **kwargs): 
    if DEBUG: print(*args, **kwargs)

INPUT = 'day22_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            num_active -= 1
            
            nexts = cycle(islice(nexts, num_active))

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

@lru_cache(maxsize=None)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def geometric(n,b,m):
    # https://stackoverflow.com/a/42033401/2734389
    T=1
    e=b%m
    total = 0
    while n>0:
        if n&1==1:
            total = (e*total + T)%m
        T = ((e+1)*T)%m
        e = (e*e)%m
        n = n//2
        #print '{} {} {}'.format(total,T,e)
    return total

def parse(lines: List[str]):
    # num_cards = 10
    # num_iters = 1
    num_cards = 119315717514047
    num_iters = 101741582076661
    params = [1, 0]
    for l in reversed(lines):
        if 'cut' in l:
            n = ints(l)[0]
            params[1] += n
        elif 'new stack' in l:
            params[0] *= -1
            params[1] *= -1
            params[1] -= 1
        elif 'deal with increment' in l:
            n = ints(l)[0]
            params[0] *= modinv(n, num_cards)
            params[1] *= modinv(n, num_cards)
    
    params[0] %= num_cards 
    params[1] %= num_cards

    print('params', params)

    # this gives us a general formula of the form 
    # src_pos = a * dst_pos + b where [a, b] are in params.
    # iterating this k times yields
    # src_pos = a^k * dst_pos + \sum_i^{k-1} a^i b
    
    def src_pos(pos):
        x = pow(params[0], num_iters, num_cards) * pos
        x += geometric(num_iters, params[0], num_cards) * params[1]
        return x % num_cards

    if num_cards < 100:
        print([src_pos(i) for i in range(num_cards)])
    print(src_pos(2020))
    return
    
    # if iteration % 10 == 0: print(iteration, target)
    # for l in reversed(lines):
    #     if 'cut' in l:
    #         n = ints(l)[0]
    #         if n > 0:
    #             if target < n: # target was part of the cut cards
    #                 target += num_cards - n
    #             else:
    #                 target -= n
    #         else: 
    #             n = -n
    #             if target >= num_cards - n:
    #                 target += (num_cards - n)
    #             else:
    #                 target -= n
    #         target %= num_cards
    #     elif 'new stack' in l:
    #         target = num_cards -1 - target
    #     elif 'deal with increment' in l:
    #         n = ints(l)[0]
    #         # if deal_round is 0, card was dealt in the first run through the deck.
    #         # deal_round = target % n
    #         # deal_shift = target // n
    #         target = (modinv(n, num_cards) * target) % num_cards
    #     # print('after undoing', repr(l), target)
    # if target in seen: print('               ', target)
    # print(target)
    print('the card finishing at position', the_target, 'is predicted to have come from position', target)

    cards = blist(range(num_cards))
    seen = set()
    # for iteration in count():
    for l in lines:
        # print(cards)
        if 'new stack' in l:
            cards.reverse()
        elif 'cut ' in l:
            n = ints(l)[0]
            if n > 0:
                cut_part = cards[:n]
                cards = (cards[n:] + cut_part)
            else: 
                n = -n
                cut_part = cards[-n:]
                cards = cut_part + cards[:-n]
        elif 'deal with increment' in l:
            n = ints(l)[0]

            new_cards = blist([None] * len(cards))
            i = 0
            for c in cards:
                new_cards[i] = c 
                i += n
                i %= len(cards)
            cards = new_cards


            # parts = chunks(cards, n)
            # cards = blist(roundrobin(*parts))
        else: 
            assert False, l
        if None in cards:
            break
    print('real', cards[the_target])
    # print(cards)
        # # print(cards[2020], end='')
        # the_card = cards[2020]
        # if the_card in seen:
        #     print('!', end='')
        # seen.add(the_card)
        # print(' ', end='')
        # if iteration % 10 == 0: print()




def solve_1(data):
    print(data)

def solve_2(data):
    pass 

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))