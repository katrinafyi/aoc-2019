from util import * 
from collections import defaultdict, deque, namedtuple
# import math
# from statistics import mean



DAY = '02'

# import numpy as np 
# import scipy as sp

def parse(file):
    return [int(x) for x in file.read().strip().split(',')]

def run_prog(a, b, data):
    data = list(data)
    index = 0
    data[1] = a
    data[2] = b
    while index < len(data):
        #print(index, data[index])
        if data[index] == 99: 
            #print('EXIT')
            break
        else: # 1 or 2
            assert data[index] == 1 or data[index] == 2
            a = data[data[index+1]]
            b = data[data[index+2]]
            out_pos = data[index+3]
            
            #print(out_pos, out_pos % 4)
            if data[index] == 1:
                data[out_pos] = a + b
            else:
                data[out_pos] = a * b
        
        index += 4
    return data[0]

def solve_1(data):
    return run_prog(12, 2, data)

def solve_2(data):
    for x in range(100):
        for y in range(100):
            result = None
            try:
                result = run_prog(x, y, data)
            except Exception as e:
                print(x,y,'failed', e)
                continue

            #print(x,y,result)
            if result == 19690720: 
                return (x,y)

if __name__ == "__main__":
    #solve_1([1,0,0,0,99])
    #solve_1([2,4,4,5,99,0])

    with open(f'day{DAY}_input.txt') as f:
        print('sol 1:', solve_1(parse(f)))
        print()
        f.seek(0)
        print('sol 2:', solve_2(parse(f)))