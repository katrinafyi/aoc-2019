import math
import operator

from math import gcd
from functools import lru_cache, reduce
from collections import namedtuple, defaultdict
from typing import Tuple, Iterator, Iterable, NamedTuple, List
from itertools import count

import re

def binary_search(test_function, exponent, debug=False):
    """ Returns the largest integer such that test_function(i) is True.

    Binary searches the range 0, ..., 2^exponent.
    Assumes test_function is a monotonic function.
    """
    max_true = -1
    basis = 2**exponent
    current = basis*2
    while basis >= 0:
        res = test_function(current)
        if debug: print('binary_search: ', current, res)
        if not res:
            current -= basis
        else:
            max_true = max(max_true, current)
            current += basis
        if basis == 0: break
        basis //= 2
    if debug: print(' returned:', max_true)
    return max_true

def binary_search_up(test_function, debug=False):
    for exponent in count(1):
        x = 2**exponent
        if not test_function(x):
            return binary_search(test_function, exponent-1, debug)


def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_many(args):
    return reduce(lcm, args)

def gcd_many(args):
    return reduce(gcd, args)

def prod(x):
    return reduce(operator.mul, x, 1)

def lmap(f, x):
    return list(map(f, x))

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

def sign(x):
    if x == 0: return 0
    return 1 if x > 0 else -1

def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]

@lru_cache(maxsize=None)
def digits(num, output_len=None):
    out = []
    i = 0
    while True:
        out.append(num % 10)
        num //= 10
        i += 1
        if (output_len is not None and i >= output_len) or num == 0:
            break 
    for _ in range(output_len - i):
        out.append(0)
    out.reverse()
    return tuple(out)
    

@lru_cache()
def count_freq(obj):
    out = {}
    for x in obj:
        if x not in out: 
            out[x] = 0
        out[x] += 1
    return out

CARDINALS = {
    'N': (0, -1),
    'S': (0, 1),
    'W': (-1, 0),
    'E': (1, 0)
}

def neighbours(pos: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    for s in CARDINALS.values():
        yield (pos[0] + s[0], pos[1] + s[1])

def tup_add(x, y) -> Tuple[int]:
    assert len(x) == len(y)
    return tuple(xi + yi for xi, yi in zip(x, y))

def tup_sub(x, y) -> Tuple[int]:
    assert len(x) == len(y)
    return tuple(xi - yi for xi, yi in zip(x, y))

def tup_mul(x, y):
    return tuple(xi * yi for xi, yi in zip(x, y))

def tup_smul(k, x):
    return tuple(k * xi for xi in x)

def euclidean(p1, p2):
    return sum((x-y)**2 for x, y in zip(p1, p2))**0.5

def manhattan(p1, p2):
    return sum(abs(x-y) for x, y in zip(p1, p2))

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

class Maxer:
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