from aoc import *
import numpy as np

data = (load(9,2023).split(' ').toint())
dtype = np.longlong

def idiff(inpt: np.ndarray, times: int):
    outpt = inpt
    for i in range(times):
        outpt = outpt[1:]-outpt[:-1]
    return outpt

def extrapolate(ys: np.ndarray, order):
    value = 0
    diffs = []
    for i in range(order+1):
        D = idiff(ys,order-i)[-1]
        diffs.append(D)
        value = value + D
    return value

sumv1 = 0
sumv2 = 0
for _list in data:
    diffdata = np.array([x for x in _list]).astype(dtype)
    n = 0
    while not all([x==0 for x in diffdata]):
        diffdata = diffdata[1:]-diffdata[:-1]
        n += 1
    
    arry = np.array([x for x in _list]).astype(dtype)
    sumv1 += extrapolate(arry,n)
    sumv2 += extrapolate(arry[::-1],n)
    
print(f'Part1: {sumv1}, Part2: {sumv2}')