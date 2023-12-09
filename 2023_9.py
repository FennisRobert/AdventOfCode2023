from aoc import *
import numpy as np
from scipy.linalg import solve

data = (load(9,2023,False).split(' ').toint())
dtype = np.float64

def extrapoly(ys: np.ndarray, order: int,):
    xs = np.arange(len(ys)).astype(dtype)
    N = order+1
    M = np.zeros((N,N)).astype(dtype)
    for i in range(N):
        M[:,i] = xs[:N]**(order-i)
    B = ys[:N]
    #coeff = np.linalg.inv(M) @ B
    coeff = solve(M, B)
    return sum(coeff*(len(ys)**np.arange(order,-1,-1).astype(np.float64))),sum(coeff*((-1)**np.arange(order,-1,-1).astype(np.float64)))

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
sumv1linalg = 0
sumv2linalg = 0
for _list in data:
    diffdata = np.array([x for x in _list])
    n = 0
    while not all([x==0 for x in diffdata]):
        diffdata = diffdata[1:]-diffdata[:-1]
        n += 1
    
    arry = np.array([x for x in _list])
    sumv1 += extrapolate(arry,n)
    sumv2 += extrapolate(arry[::-1],n)
    p1, p2 = extrapoly(arry,n)
    sumv1linalg += p1
    sumv2linalg += p2
    extrapoly(arry,n)
    
print(f'Part1: {sumv1}, Part2: {sumv2}')
print(f'Part1 LinAlg: {round(sumv1linalg)}, Part2 LinAlg: {round(sumv2linalg)}')