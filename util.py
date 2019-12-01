import math

from collections import namedtuple
from typing import Tuple, Iterator, Iterable, NamedTuple, List

_shifts = ( (0, 1), (0, -1), (1, 0), (-1, 0) )
def adjacents(pos: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    for s in _shifts:
        yield (pos[0] + s[0], pos[1] + s[1])

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