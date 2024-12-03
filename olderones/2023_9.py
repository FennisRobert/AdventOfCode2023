from aoc import *
import numpy as np
from scipy.linalg import solve
import matplotlib.pyplot as plt

data = (load(9,2023,False).split(' ').toint())
dtype = np.float64

def extrapoly(ys: np.ndarray, order: int, querypoint):
    xs = np.arange(len(ys)).astype(dtype)
    N = order+1
    M = np.zeros((N,N)).astype(dtype)
    for i in range(N):
        M[:,i] = xs[:N]**(order-i)
    B = ys[:N]
    coeff = solve(M, B)
    return sum(coeff*(querypoint**np.arange(order,-1,-1).astype(np.float64)))


def plotsol(ys: np.ndarray, order: int, querypoint):
    xs = np.arange(len(ys)).astype(dtype)
    N = order+1
    M = np.zeros((N,N)).astype(dtype)
    for i in range(N):
        M[:,i] = xs[:N]**(order-i)
    B = ys[:N]
    coeff = solve(M, B)
    
    xs = xs[:5]
    ys = ys[:5]
    f = lambda x: x#np.log10(x)
    plt.scatter(xs, f(ys))
    DX = xs[-1]
    xs2 = np.linspace(-1, xs[-1]+1.2,10000)

    ys2 = sum([(xs2**(order-i))*coeff[i] for i in range(N)])
    x3 = np.array([-1, xs[-1]+1])
    y3 = sum([(x3**(order-i))*coeff[i] for i in range(N)])
    
    plt.plot(xs2,f(ys2))
    plt.scatter(x3,f(y3))
    plt.grid(True)
    plt.show()
    


    
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

N=data.len-2

for i, _list in enumerate(data):
    diffdata = np.array([x for x in _list])
    n = 0
    while not all([x==0 for x in diffdata]):
        diffdata = diffdata[1:]-diffdata[:-1]
        n += 1
    
    arry = np.array([x for x in _list])
    
    sumv1 += extrapolate(arry,n)
    sumv2 += extrapolate(arry[::-1],n)
    
    sumv1linalg += extrapoly(arry,n,len(arry))
    sumv2linalg += extrapoly(arry,n,-1)
    plotsol(arry,n,len(arry))

    

    
print(f'Part1: {sumv1}, Part2: {sumv2}')
print(f'Part1 LinAlg: {round(sumv1linalg)}, Part2 LinAlg: {round(sumv2linalg)}')