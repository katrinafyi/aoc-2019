from itertools import *
from functools import reduce

from collections.abc import Iterable, Iterator

class San(object):
    def __new__(cls, iterator):
        if isinstance(iterator, Iterator):
            #print(iterator, 'is iterator')
            x = super(San, cls).__new__(cls)
            x.__init__(iterator)
            return x
        elif isinstance(iterator, Iterable):
            #print(iterator, 'is iterable')
            x = super(San, cls).__new__(cls)
            iterator = iter(iterator)
            x.__init__(iterator)
            return x
        #print(iterator, 'NOT')
        return iterator
    def __init__(self, iterator):
        if not hasattr(self, 'iterator'):
            self.iterator = iterator
    def collect(self):
        return list(self)
    def first(self):
        return next(self.iterator)
    def __iter__(self):
        return self.iterator
    def __repr__(self):
        return f'San({repr(self.iterator)})'

_class_methods = [
    count, cycle, repeat, product, permutations, combinations,
    combinations_with_replacement, zip, chain, sum, max, min, range,

    # instance methods where argument is first are effectively a class method.
    accumulate, compress, islice,  
]

_second_arg = [
    map, filter, dropwhile, filterfalse, groupby, takewhile, zip_longest, starmap
]

for f in _class_methods:
    setattr(San, f.__name__, lambda *args, f=f, **kwargs: San(f(*args, **kwargs)))

# for f in _first_arg:
#     setattr(San, f.__name__, 
#         lambda self, *args, f=f, **kwargs: San(f(self, *args, **kwargs)))

for f in _second_arg:
    setattr(San, f.__name__, 
        lambda self, *args, f=f, **kwargs: San(f(*(args[:1] + (self,) + args[1:]), **kwargs)))

if __name__ == '__main__':
    print(San.count().islice(None, 10).filter(lambda x: x % 2 == 0).first())
    print(San.chain((1,2,3), (4,3,2)).map(lambda a: 2).collect())
    print(iter(San.range(7)))
    print(San.count(15).islice(1, 10).map(lambda x: x**2).zip(San.count(), San.count(10, 2)).collect())
    print(San.zip(San.range(4), San.repeat(2)).starmap(pow).sum())
    map(lambda x: x*2, map(int, [1, 2]))