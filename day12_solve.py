from util import * 
from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass, field
from typing import *
import sys
# from statistics import mean

INPUT = 'day12_input.txt' if len(sys.argv) == 1 else sys.argv[1]

# import numpy as np 
# import scipy as sp

def parse(lines: List[str]):
    return [ints(x) for x in lines]

@dataclass(frozen=1)
class Moon:
    pos: list = field(default_factory=tuple)
    velocity: list = field(default_factory=lambda: tuple([0, 0, 0]))

def solve_1(data):
    moons = tuple([Moon(tuple(x)) for x in data])

    for t in range(1000):
        # print('after', t)
        # for m in moons: print(m)

        moons2 = []
        for m in moons:
            vel = list(m.velocity)
            for m2 in moons:
                if m2 == m: continue 
                i = 0
                for a, b in zip(m.pos, m2.pos):
                    vel[i] += sign(b - a)
                    i += 1
            vel = tuple(vel)
            
            moons2.append(Moon(tup_add(m.pos, vel), vel))
        moons = moons2

    E = 0
    for m in moons:
        E += sum(map(abs, m.pos)) * sum(map(abs, m.velocity))
    return E

def solve_2(data):
    moons = tuple([Moon(tuple(x)) for x in data])

    periods = []
    for dim in range(3):
        xs = [m.pos[dim] for m in moons]
        deltas = [0]*4
        print(xs)

        seen = set()
        prev = None
        for t in range(10000000000):
            for i in range(4): 
                this = xs[i]
                v = deltas[i]
                for j in range(4):
                    v += sign(xs[j] - this)
                deltas[i] = v
            
            for i in range(4):
                xs[i] += deltas[i]
            #print(t, xs)
            tup = tuple(xs) + tuple(deltas)
            if tup in seen: 
                print(dim, ' repeat at', t)
                if prev is not None:
                    print('  delta:', t - prev)
                    break
                prev = t
                seen.clear()
            seen.add(tup)
        periods.append(t - prev)
    print(periods)
    return lcm_many(periods)

if __name__ == "__main__":
    with open(INPUT) as f:
        print('sol 1:', solve_1(parse(f.readlines())))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f.readlines())))