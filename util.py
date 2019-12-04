import math

from functools import lru_cache
from collections import namedtuple, defaultdict
from typing import Tuple, Iterator, Iterable, NamedTuple, List

import re

INT_REGEX = re.compile(r'-?\d+')
UINT_REGEX = re.compile(r'\d+')
def ints(s: str) -> List[int]:
    return map_int(INT_REGEX.findall(s))

def uints(s):
    return map_int(UINT_REGEX.findall(s))

def map_int(l) -> List[int]:
    return [int(x) for x in l]

def map_float(l) -> List[int]:
    return [float(x) for x in l]

@lru_cache()
def count_freq(obj):
    out = {}
    for x in obj:
        if x not in out: 
            out[x] = 0
        out[x] += 1
    return out

CARDINALS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}

def adjacents(pos: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    for s in CARDINALS.values():
        yield (pos[0] + s[0], pos[1] + s[1])

def tup_add(x, y) -> Tuple[int]:
    assert len(x) == len(y)
    return tuple(xi + yi for xi, yi in zip(x, y))

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

MinMax = namedtuple('MinMax', ('min', 'max'))

def min_max_tuples(tuples: Iterable[Tuple]) -> List[MinMax]:
    """Returns the min and max of values in each column in a given list of 
    tuples.
    
    Arguments:
        tuples {Iterable[Tuple]} -- Iterable of tuples.
    
    Returns:
        List[MinMax] -- List of MinMax. The MinMax in the i-th position 
        has the min/max values for values of the input tuples in the i-th position.
    """

    mins = None
    maxs = None
    for tuple_ in tuples:
        if mins is None:
            mins = [math.inf]*len(tuple_)
            maxs = [-math.inf]*len(tuple_)
        for i, val in enumerate(tuple_):
            if val < mins[i]:
                mins[i] = val 
            if val > maxs[i]:
                maxs[i] = val
    
    return [MinMax(mins[i], maxs[i]) for i in range(len(mins))]

class Maximiser:
    def __init__(self, is_max=True):
        self.key = None 
        self.value = None
        self.max = is_max
    
    def update(self, key, value):
        if self.key is None or ((value > self.value) if self.max else (value < self.value)):
            self.key = key 
            self.value = value

    def get_max(self):
        return (self.key, self.value)